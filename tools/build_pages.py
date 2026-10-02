"""Stage allowlisted committed lessons and build the GitHub Pages reading edition."""

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote, urljoin, urlsplit

from export_wiki import (
    Links, REPOSITORY, ROOT, Snapshot, chapter_navigation, checked_output,
    page_map, rewrite_markdown,
)


SITE_URL = "https://anowarislam.github.io/rack-scale-ai-infrastructure/"
GENERATOR = "rack-scale-course-pages-v1"
MANIFEST = "course-manifest.json"
OWNER = ".pages-build.json"
ASSETS = {"site_src/index.md": "index.md", "site_src/stylesheets/course.css": "stylesheets/course.css"}


class PageLinks(Links):
    def __init__(self, snapshot, pages):
        super().__init__(snapshot, {source: name + ".md" for source, name in pages.items()})
        # The existing rewriter validates paths and pins non-page links. MkDocs
        # needs relative Markdown destinations so it can check and relocate them.
        self.wiki = ""


def prepare_markdown(text):
    """Enable Markdown in answer disclosures, without touching code examples."""
    output, fence = [], None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
        elif marker:
            fence = marker[1]
        elif line.rstrip("\r\n") == "<details>":
            line = line.replace("<details>", '<details markdown="1">')
        output.append(line)
    return "".join(output)


def render(snapshot, asset_root=ROOT):
    pages = page_map()
    course = json.loads(snapshot.read("course-map.json"))
    chapters = [course["bridge"]] + [p for month in course["months"] for p in month["lessons"]]
    if len(pages) != 61 or len(chapters) != 30 or len(set(chapters)) != 30 or not set(chapters) <= pages.keys():
        raise ValueError("Expected 61 source pages and all 30 distinct teaching chapters")
    links, navigation = PageLinks(snapshot, pages), chapter_navigation(course)
    rendered, hashes = {}, {}
    for source, name in pages.items():
        original = snapshot.read(source)
        hashes[source] = hashlib.sha256(original.encode()).hexdigest()
        body = prepare_markdown(rewrite_markdown(original, lambda target: links.rewrite(target, source)))
        footer = ["[Course home](index.md)", links.page("CALENDAR.md", "Study calendar")]
        for label, targets in zip(("Previous", "Next"), navigation.get(source, ([], []))):
            footer.extend(links.page(p, f"{label}: {pages[p].replace('-', ' ')}") for p in targets)
        footer.append(f"[Source Markdown]({links.source_url(source)})")
        rendered[name + ".md"] = body.rstrip() + "\n\n---\n\n" + " | ".join(footer) + "\n"
    # These two presentation assets may be previewed before committing. Lesson
    # content is always read from the resolved commit, never from the worktree.
    for source, target in ASSETS.items():
        path = asset_root / source
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Missing or symlinked presentation asset: {source}")
        rendered[target] = path.read_text(encoding="utf-8")
    for name, value in (("SOURCE_COMMIT", snapshot.ref), ("SOURCE_SHORT", snapshot.ref[:12]), ("REPOSITORY", REPOSITORY)):
        rendered["index.md"] = rendered["index.md"].replace("{{" + name + "}}", value)
    if re.search(r"\{\{[^}]+\}\}", rendered["index.md"]):
        raise ValueError("Unresolved placeholder in course homepage")
    manifest = {
        "generator": GENERATOR, "source_repository": REPOSITORY, "source_ref": snapshot.ref,
        "pages": {source: name + ".md" for source, name in pages.items()},
        "source_sha256": hashes,
        "presentation_sha256": {target: hashlib.sha256(rendered[target].encode()).hexdigest() for target in ASSETS.values()},
        "teaching_chapters": chapters,
    }
    rendered[MANIFEST] = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    return rendered, manifest


def owned_directory(path):
    """Refuse unmanaged or symlinked output before allowing a clean build."""
    path = checked_output(ROOT, path)
    if path.exists():
        if not path.is_dir() or any(p.is_symlink() for p in path.rglob("*")):
            raise ValueError(f"Unsafe output directory: {path}")
        if any(path.iterdir()):
            marker = path / OWNER
            if not marker.is_file() or json.loads(marker.read_text()).get("generator") != GENERATOR:
                raise ValueError(f"Refusing unmanaged output directory: {path}")
    path.mkdir(parents=True, exist_ok=True)
    (path / OWNER).write_text(json.dumps({"generator": GENERATOR}) + "\n")
    return path


def stage(rendered):
    output = owned_directory(ROOT / ".cache/pages-docs")
    for item in output.iterdir():
        if item.name != OWNER:
            shutil.rmtree(item) if item.is_dir() else item.unlink()
    for name, body in rendered.items():
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
    return output


def on_nav(nav, *, config, files):
    """Keep theme metadata on the same chapter route as the visible navigation."""
    manifest = json.loads((Path(config.docs_dir) / MANIFEST).read_text())
    snapshot = Snapshot(ROOT, manifest["source_ref"])
    navigation = chapter_navigation(json.loads(snapshot.read("course-map.json")))
    by_name = {page.file.src_uri: page for page in nav.pages}
    for page in nav.pages:
        page.previous_page = page.next_page = None
    for source, (previous, following) in navigation.items():
        page = by_name[manifest["pages"][source]]
        if len(previous) == 1:
            page.previous_page = by_name[manifest["pages"][previous[0]]]
        if len(following) == 1:
            page.next_page = by_name[manifest["pages"][following[0]]]
    return nav


class HtmlReferences(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.links, self.ids = [], set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.ids.update(attrs[name] for name in ("id", "name") if attrs.get(name))
        self.links.extend(attrs[name] for name in ("href", "src") if attrs.get(name))


def validate_site(output, manifest):
    """Check actual HTML targets, including raw HTML links and fragment IDs."""
    html = {p.relative_to(output).as_posix(): HtmlReferences(p.read_text()) for p in output.rglob("*.html")}
    expected = {"index.html"} | {name.removesuffix(".md") + "/index.html" for name in manifest["pages"].values()}
    if set(html) != expected | {"404.html"}:
        raise ValueError("Built HTML coverage differs from the explicit publication allowlist")
    origin, base = urlsplit(SITE_URL).netloc, urlsplit(SITE_URL).path
    count = 0
    for filename, document in html.items():
        text = (output / filename).read_text()
        if re.search(r"file://|/Users/|/home/[^ /\s]+/", text):
            raise ValueError(f"Local machine path in published HTML: {filename}")
        page_url = urljoin(SITE_URL, filename.removesuffix("index.html"))
        for target in document.links:
            resolved = urlsplit(urljoin(page_url, target))
            if resolved.netloc != origin:
                continue
            if not resolved.path.startswith(base):
                raise ValueError(f"Link escapes the Pages base path in {filename}: {target}")
            relative = unquote(resolved.path[len(base):]) or "index.html"
            if relative.endswith("/"):
                relative += "index.html"
            path = output / relative
            if not path.is_file():
                raise ValueError(f"Missing built target in {filename}: {target}")
            fragment = unquote(resolved.fragment)
            if fragment and relative in html and fragment not in html[relative].ids:
                raise ValueError(f"Missing built anchor in {filename}: {target}")
            count += 1
    if not (output / "search/search_index.json").is_file():
        raise ValueError("Search index was not built")
    if json.loads((output / MANIFEST).read_text()) != manifest:
        raise ValueError("Published source manifest differs from the staged edition")
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-ref", default="HEAD", help="Committed lesson revision, resolved to a full SHA")
    parser.add_argument("--prepare-only", action="store_true", help="Stage committed lessons for mkdocs serve")
    args = parser.parse_args()
    try:
        snapshot = Snapshot(ROOT, args.source_ref)
        rendered, manifest = render(snapshot)
        stage(rendered)
        print(f"PASS: staged 61 source pages, 1 homepage, 30 teaching chapters from {snapshot.ref}", flush=True)
        if not args.prepare_only:
            output = owned_directory(ROOT / ".cache/pages-site")
            try:
                subprocess.run([sys.executable, "-m", "mkdocs", "build", "--strict", "--clean", "--config-file", str(ROOT / "mkdocs.yml")], cwd=ROOT, check=True)
            finally:
                (output / OWNER).write_text(json.dumps({"generator": GENERATOR}) + "\n")
            count = validate_site(output, manifest)
            print(f"PASS: built 62 reading pages; checked {count} local HTML links/assets and their anchors")
            print(f"Output: {output}\nSource: {snapshot.ref}")
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
