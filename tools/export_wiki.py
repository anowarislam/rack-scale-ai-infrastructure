"""Export a committed course snapshot to a controlled GitHub Wiki staging directory."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import subprocess
import sys
from urllib.parse import quote, unquote, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/anowarislam/rack-scale-ai-infrastructure"
GENERATOR = "rack-scale-course-wiki-v1"
MANIFEST = "wiki-export-manifest.json"
EXCLUDED = {".git", ".cache", ".worktrees", ".superpowers", "__pycache__", "learner-work"}

# Explicit publication allowlist. New Markdown files do not become wiki pages by default.
PAGE_SPECS = (
    ("LEARNING-GUIDE.md", "Learning-Guide"),
    ("CALENDAR.md", "Study-Calendar"),
    ("curriculum/00-bridge.md", "00-Fundamentals-Bridge"),
    ("curriculum/01-system-map.md", "01-System-Map"),
    ("curriculum/02-server-control.md", "02-Server-Control"),
    ("curriculum/03-gpu-runtime.md", "03-GPU-Runtime"),
    ("curriculum/04-fabric-storage.md", "04-Fabric-and-Storage"),
    ("curriculum/05-power-telemetry-security.md", "05-Power-Telemetry-and-Security"),
    ("curriculum/06-workloads.md", "06-Workloads"),
    ("curriculum/07-workload-contract.md", "07-Workload-Contract"),
    ("tracks/kubernetes/README.md", "Kubernetes-Track"),
    ("tracks/kubernetes/08-reference-environment.md", "Kubernetes-08-Reference-Environment"),
    ("tracks/kubernetes/09-placement-and-fairness.md", "Kubernetes-09-Placement-and-Fairness"),
    ("tracks/kubernetes/10-workload-recovery.md", "Kubernetes-10-Workload-Recovery"),
    ("tracks/kubernetes/11-operability.md", "Kubernetes-11-Operability"),
    ("tracks/kubernetes/12-integration-and-comparison.md", "Kubernetes-12-Integration-and-Comparison"),
    ("tracks/slurm/README.md", "Slurm-Track"),
    ("tracks/slurm/08-reference-environment.md", "Slurm-08-Reference-Environment"),
    ("tracks/slurm/09-placement-and-fairness.md", "Slurm-09-Placement-and-Fairness"),
    ("tracks/slurm/10-workload-recovery.md", "Slurm-10-Workload-Recovery"),
    ("tracks/slurm/11-operability.md", "Slurm-11-Operability"),
    ("tracks/slurm/12-integration-and-comparison.md", "Slurm-12-Integration-and-Comparison"),
    ("curriculum/13-fleet-truth.md", "13-Fleet-Truth"),
    ("curriculum/14-reliability.md", "14-Reliability"),
    ("curriculum/15-incidents-and-change.md", "15-Incidents-and-Change"),
    ("curriculum/16-lifecycle-automation.md", "16-Lifecycle-Automation"),
    ("curriculum/17-capacity-and-readiness.md", "17-Capacity-and-Readiness"),
    ("curriculum/18-specialty-integration.md", "18-Specialty-Integration"),
    ("assessments/gates.md", "Assessment-Gates"),
    ("assessments/progress-template.md", "Progress-Template"),
    ("assessments/evidence-template.md", "Evidence-Template"),
    ("specialties/README.md", "Specialties"),
    ("specialties/rack-lifecycle.md", "Specialty-Rack-Lifecycle"),
    ("specialties/performance.md", "Specialty-Performance"),
    ("specialties/workload-platform.md", "Specialty-Workload-Platform"),
    ("specialties/fleet-automation.md", "Specialty-Fleet-Automation"),
    ("practicum/README.md", "Practicum"),
    ("practicum/19-inherit.md", "19-Inherit-and-Baseline"),
    ("practicum/20-performance.md", "20-Cross-Layer-Performance"),
    ("practicum/21-recovery.md", "21-Compound-Recovery"),
    ("practicum/22-rack-readiness.md", "22-Rack-Readiness"),
    ("practicum/23-portfolio.md", "23-Portfolio-Decision"),
    ("practicum/24-defense.md", "24-Final-Defense"),
    ("practicum/capstones/README.md", "Capstones"),
    ("practicum/capstones/engineer.md", "Capstone-Engineer"),
    ("practicum/capstones/aspiring-leader.md", "Capstone-Aspiring-Leader"),
    ("practicum/capstones/manager.md", "Capstone-Manager"),
    ("practicum/instructor/19-key.md", "Instructor-19-Key"),
    ("practicum/instructor/20-key.md", "Instructor-20-Key"),
    ("practicum/instructor/21-key.md", "Instructor-21-Key"),
    ("practicum/instructor/22-key.md", "Instructor-22-Key"),
    ("practicum/instructor/23-key.md", "Instructor-23-Key"),
    ("practicum/instructor/24-key.md", "Instructor-24-Key"),
    ("practicum/l2-recovery-runbook.md", "Two-Host-Recovery-Runbook"),
    ("labs/systems/README.md", "Systems-Labs"),
    ("labs/systems/hardware-workbook.md", "Hardware-Workbook"),
    ("labs/platforms/README.md", "Platform-Labs"),
    ("labs/platforms/kubernetes/README.md", "Kubernetes-Lab"),
    ("labs/platforms/slurm/runbook.md", "Slurm-Lab"),
    ("labs/fleet/README.md", "Fleet-Labs"),
    ("evidence/README.md", "Sources-and-Evidence"),
)


def page_map(specs=PAGE_SPECS):
    pages, names = {}, {"home", "_sidebar", "_footer"}
    for source, name in specs:
        path = PurePosixPath(source)
        if (path.is_absolute() or ".." in path.parts or EXCLUDED.intersection(path.parts)
                or path.suffix != ".md" or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*", name)):
            raise ValueError(f"Unsafe publication entry: {source} -> {name}")
        if source in pages or name.casefold() in names:
            raise ValueError(f"Duplicate source or wiki page collision: {source} -> {name}")
        pages[source] = name
        names.add(name.casefold())
    return pages


class Snapshot:
    def __init__(self, root, source_ref):
        self.root = root
        self.ref = self.git("rev-parse", "--verify", f"{source_ref}^{{commit}}").strip()
        self.files = {}
        self.directories = {"."}
        for entry in self.git("ls-tree", "-rz", "--full-tree", self.ref).split("\0"):
            if not entry:
                continue
            metadata, path = entry.split("\t", 1)
            self.files[path] = metadata.split()[0]
            self.directories.update(str(p) for p in PurePosixPath(path).parents)

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], text=True)

    def read(self, path):
        if self.files.get(path) not in {"100644", "100755"}:
            raise ValueError(f"Not a regular tracked file at {self.ref}: {path}")
        return self.git("show", f"{self.ref}:{path}")


class Links:
    def __init__(self, snapshot, pages, repository=REPOSITORY):
        self.snapshot, self.pages, self.repository = snapshot, pages, repository
        self.wiki = repository + "/wiki/"

    def source_url(self, path):
        kind = "blob" if path in self.snapshot.files else "tree"
        if path not in self.snapshot.files and path not in self.snapshot.directories:
            raise ValueError(f"Untracked or missing source link: {path}")
        return f"{self.repository}/{kind}/{self.snapshot.ref}/{quote(path, safe='/')}"

    def page(self, source, label=None):
        return f"[{label or self.pages[source]}]({self.wiki}{self.pages[source]})"

    def rewrite(self, target, source):
        # Markdown escapes are syntax, not characters in the source path.
        plain = re.sub(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])", r"\1", target)
        parts = urlsplit(plain)
        if parts.scheme == "file":
            raise ValueError(f"Local file URL in {source}: {target}")
        if parts.scheme or parts.netloc or not parts.path:
            return target
        decoded = unquote(parts.path)
        if decoded.startswith(("/", "\\")) or "\\" in decoded:
            raise ValueError(f"Absolute or non-POSIX source link in {source}: {target}")
        path = posixpath.normpath(posixpath.join(posixpath.dirname(source), decoded))
        if path == ".." or path.startswith("../") or EXCLUDED.intersection(PurePosixPath(path).parts):
            raise ValueError(f"Link escapes publishable source in {source}: {target}")
        base = self.wiki + self.pages[path] if path in self.pages else self.source_url(path)
        return urlunsplit((*urlsplit(base)[:3], parts.query, parts.fragment))


def rewrite_prose(text, rewrite):
    """Rewrite inline destinations and reference definitions, preserving other syntax."""
    def reference(match):
        target = match[2]
        return match[1] + ("<" + rewrite(target[1:-1]) + ">" if target.startswith("<") else rewrite(target))

    text = re.sub(r"(?m)^( {0,3}\[[^\]\n]+\]:[ \t]*)(<[^>\n]*>|[^\s]+)", reference, text)
    replacements = []
    for match in re.finditer(r"(?<!\\)\]\([ \t\n]*", text):
        start = end = match.end()
        if start == len(text):
            continue
        if text[start] == "<":
            start += 1
            end = text.find(">", start)
            if end == -1:
                continue
        else:
            depth = 0
            while end < len(text):
                char = text[end]
                if char == "\\" and end + 1 < len(text):
                    end += 2
                    continue
                if char == "(":
                    depth += 1
                elif char == ")":
                    if depth == 0:
                        break
                    depth -= 1
                elif char.isspace() and depth == 0:
                    break
                end += 1
        if end > start:
            replacements.append((start, end, rewrite(text[start:end])))
    for start, end, replacement in reversed(replacements):
        text = text[:start] + replacement + text[end:]
    return text


def rewrite_markdown(text, rewrite):
    """Keep fenced/indented code and exact-length inline code spans byte-for-byte."""
    def prose(chunk):
        result, cursor = [], 0
        while match := re.search(r"`+", chunk[cursor:]):
            start = cursor + match.start()
            end = cursor + match.end()
            closing = re.search(r"(?<!`)" + re.escape(match[0]) + r"(?!`)", chunk[end:])
            if not closing:
                break
            stop = end + closing.end()
            result.extend((rewrite_prose(chunk[cursor:start], rewrite), chunk[start:stop]))
            cursor = stop
        return "".join(result) + rewrite_prose(chunk[cursor:], rewrite)

    output, pending, fence = [], [], None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        code = fence is not None or marker is not None or line.startswith(("    ", "\t"))
        if code:
            output.append(prose("".join(pending)))
            pending = []
            output.append(line)
            if fence and marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            elif fence is None and marker:
                fence = marker[1]
        else:
            pending.append(line)
    return "".join(output) + prose("".join(pending))


def chapter_navigation(course):
    months = course["months"]
    nav = {course["bridge"]: ([], months[0]["lessons"])}
    for index, month in enumerate(months):
        for source in month["lessons"]:
            before = months[index - 1]["lessons"] if index else [course["bridge"]]
            after = months[index + 1]["lessons"] if index + 1 < len(months) else []
            track = str(PurePosixPath(source).parent)
            select = lambda paths: [p for p in paths if str(PurePosixPath(p).parent) == track] or paths
            nav[source] = (select(before), select(after))
    return nav


def render(snapshot, pages=None):
    pages = page_map() if pages is None else pages
    links = Links(snapshot, pages)
    source_text = {path: snapshot.read(path) for path in pages}
    titles = {path: text.splitlines()[0].removeprefix("# ") for path, text in source_text.items()}
    course = json.loads(snapshot.read("course-map.json"))
    chapters = [course["bridge"]] + [p for m in course["months"] for p in m["lessons"]]
    if len(chapters) != 30 or len(set(chapters)) != 30 or not set(chapters) <= pages.keys():
        raise ValueError("Expected all 30 distinct teaching chapters in the publication allowlist")
    nav = chapter_navigation(course)
    rendered = {}
    for path, name in pages.items():
        body = rewrite_markdown(source_text[path], lambda target: links.rewrite(target, path))
        navigation = [f"[Course home]({links.wiki}Home)", links.page("CALENDAR.md", "Study calendar")]
        for label, targets in zip(("Previous", "Next"), nav.get(path, ([], []))):
            navigation.extend(links.page(p, f"{label}: {pages[p].replace('-', ' ')}") for p in targets)
        navigation.append(f"[Source Markdown]({links.source_url(path)})")
        rendered[name + ".md"] = body.rstrip() + "\n\n---\n\n" + " | ".join(navigation) + "\n"

    def listing(paths):
        return "\n".join("- " + links.page(p, titles[p]) for p in paths)

    groups = (
        ("Start here", ["LEARNING-GUIDE.md", "CALENDAR.md", course["bridge"]]),
        ("Systems foundations and workload contracts", [p for p in chapters if p.startswith("curriculum/") and p != course["bridge"] and int(PurePosixPath(p).name[:2]) <= 7]),
        ("Kubernetes: months 8-12", [p for p in pages if p.startswith("tracks/kubernetes/")]),
        ("Slurm: months 8-12", [p for p in pages if p.startswith("tracks/slurm/")]),
        ("Fleet operations: months 13-18", [p for p in chapters if p.startswith("curriculum/") and int(PurePosixPath(p).name[:2]) >= 13]),
        ("Specialties: choose one", [p for p in pages if p.startswith("specialties/")]),
        ("Practicum: months 19-24", ["practicum/README.md"] + [p for p in chapters if p.startswith("practicum/")]),
        ("Assessment and capstones", [p for p in pages if p.startswith(("assessments/", "practicum/capstones/"))]),
        ("Practical work and evidence", [p for p in pages if p.startswith(("labs/", "evidence/"))] + ["practicum/l2-recovery-runbook.md"]),
        ("Instructor keys: open after your attempt", [p for p in pages if p.startswith("practicum/instructor/")]),
    )
    home = f"""# Rack-scale AI infrastructure

Learn how CPUs, GPUs, memory, networks, storage, workload platforms, and fleet operations fit together. Start with **theory, worked examples, and reasoned answers**; use practical exercises to test your explanations.

Begin with {links.page('LEARNING-GUIDE.md', 'the learning guide')}, then {links.page(course['bridge'], 'the fundamentals bridge')} and {links.page(chapters[1], 'month 1')}. The course has 24 scheduled months and 30 teaching chapters, including the bridge and both platform tracks. Select one primary platform and one specialty. The calendar is a pacing guide; progress depends on demonstrated understanding.

## Read here; run from the source repository

This wiki is the reading edition. **[Clone the source repository]({links.repository}) for all code, fixtures, configurations, and runnable exercises.** Run lesson commands from that clone's root directory.

```bash
git clone {links.repository}.git
cd rack-scale-ai-infrastructure
git checkout {snapshot.ref}
```

This edition corresponds to [source commit {snapshot.ref[:12]}]({links.repository}/commit/{snapshot.ref}). Files that are not wiki pages link to that committed snapshot. Make corrections in the source repository and regenerate the wiki.

## Follow the course

Read the common foundations first. For months 8-12, study Kubernetes or Slurm in depth and use the other track's secondary route. Continue through fleet operations, one specialty, and the integrated practicum. Reading or passing local tests does not complete a learner assessment; keep evidence of what you can explain and demonstrate.
"""
    for heading, paths in groups:
        home += f"\n### {heading}\n\n{listing(paths)}\n"
    home += f"""
The instructor keys are publicly readable and sealed only by convention. Attempt a scenario before opening its key; label key-assisted work honestly.

## Source records and scope

The [recorded validation results]({links.source_url('validation/RESULTS.md')}) distinguish executed checks from untested environments. The [delivery status]({links.source_url('DELIVERY-STATUS.md')}) records the source snapshot's delivered state. Environment fidelity and authorization limits remain in each lesson and runbook.

The [delivery decision]({links.source_url('decisions/0005-deliver-the-course.md')}) and [original charter]({links.source_url('course-charter.md')}) are project history. The source repository is authoritative for course changes; this generated edition does not confer certification, equipment access, or permission to change shared systems.
"""
    rendered["Home.md"] = home
    rendered["_Sidebar.md"] = f"**[Course home]({links.wiki}Home)**\n\n" + "\n\n".join(
        f"**{heading}**\n\n{listing(paths)}" for heading, paths in groups[:5]
    ) + "\n\n" + listing(["specialties/README.md", "practicum/README.md", "practicum/capstones/README.md", "assessments/gates.md", "labs/systems/README.md", "labs/platforms/README.md", "labs/fleet/README.md", "evidence/README.md"]) + "\n"
    rendered["_Footer.md"] = f"[Course home]({links.wiki}Home) | [Runnable source]({links.repository}) | [Edition {snapshot.ref[:12]}]({links.repository}/commit/{snapshot.ref})\n\nGenerated from the source repository. Submit corrections there; wiki edits are not the course source.\n"
    validate_links(rendered, links)
    return rendered, pages


def validate_links(rendered, links):
    valid_pages = {name.removesuffix(".md") for name in rendered}
    def check(target):
        parts = urlsplit(target)
        if target.startswith(links.wiki):
            name = unquote(parts.path.removeprefix(urlsplit(links.wiki).path))
            if name not in valid_pages:
                raise ValueError(f"Missing exported wiki page: {target}")
        elif parts.path and not parts.scheme and not parts.netloc:
            raise ValueError(f"Unconverted local link: {target}")
        elif parts.scheme == "file":
            raise ValueError(f"Local file URL in export: {target}")
        return target
    for body in rendered.values():
        rewrite_markdown(body, check)


def export_manifest(rendered, pages, snapshot):
    return {
        "generator": GENERATOR,
        "source_repository": REPOSITORY,
        "source_ref": snapshot.ref,
        "pages": {source: name + ".md" for source, name in sorted(pages.items())},
        "generated_pages": ["Home.md", "_Sidebar.md", "_Footer.md"],
        "files": {name: hashlib.sha256(body.encode()).hexdigest() for name, body in sorted(rendered.items())},
    }


def checked_output(root, output):
    """Only use a staging directory below this repository's .cache, never a wiki clone."""
    root = root.resolve()
    output = output if output.is_absolute() else root / output
    if ".." in output.parts:
        raise ValueError("Output path must not contain '..'")
    cache = root / ".cache"
    if output == cache or not output.is_relative_to(cache):
        raise ValueError("Output must be a directory below this repository's .cache")
    for path in (output, *output.parents):
        if path == root:
            break
        if path.is_symlink():
            raise ValueError(f"Refusing symlinked output path: {path}")
    return output


def write_export(root, output, rendered, manifest, check=False):
    output = checked_output(root, output)
    previous = {}
    if output.exists():
        if not output.is_dir():
            raise ValueError(f"Output is not a directory: {output}")
        entries = {p.name for p in output.iterdir()}
        if entries:
            marker = output / MANIFEST
            if marker.is_symlink() or not marker.is_file():
                raise ValueError("Nonempty output is not a managed export; no files changed")
            previous = json.loads(marker.read_text())
            if previous.get("generator") != GENERATOR or previous.get("source_repository") != REPOSITORY:
                raise ValueError("Output manifest belongs to another exporter or repository")
            old_files = previous.get("files", {})
            if entries != set(old_files) | {MANIFEST}:
                raise ValueError("Output has missing or unowned files; no files changed")
            for name, digest in old_files.items():
                if not re.fullmatch(r"(?:[A-Za-z0-9][A-Za-z0-9-]*|_Sidebar|_Footer)\.md", name):
                    raise ValueError(f"Unsafe filename in output manifest: {name}")
                path = output / name
                if path.is_symlink() or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                    raise ValueError(f"Output was edited or is unsafe: {name}; no files changed")
    payload = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    if check:
        if previous != manifest:
            raise ValueError("Export does not match the requested source snapshot; regenerate it")
        return output
    output.mkdir(parents=True, exist_ok=True)
    for name, body in rendered.items():
        (output / name).write_text(body, encoding="utf-8")
    for name in previous.get("files", {}).keys() - rendered.keys():
        (output / name).unlink()
    (output / MANIFEST).write_text(payload, encoding="utf-8")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-ref", default="HEAD", help="Committed source revision; resolved to a full commit SHA")
    parser.add_argument("--output", type=Path, default=Path(".cache/wiki-export"), help="Staging directory below repository .cache")
    parser.add_argument("--check", action="store_true", help="Validate an existing export without changing files")
    args = parser.parse_args()
    try:
        snapshot = Snapshot(ROOT, args.source_ref)
        rendered, pages = render(snapshot)
        output = write_export(ROOT, args.output, rendered, export_manifest(rendered, pages, snapshot), args.check)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"PASS: {'verified' if args.check else 'exported'} {len(pages)} source pages, 3 navigation pages, 30 teaching chapters")
    print(f"Source: {snapshot.ref}\nOutput: {output}\nManifest: {output / MANIFEST}")
    print("Scope: committed content, local link targets, and controlled staging files; remote publication is a separate step.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
