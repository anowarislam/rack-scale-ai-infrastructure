"""Validate course structure and local references; not learner mastery or prose quality."""

from collections import Counter
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".cache", ".worktrees", ".superpowers", "__pycache__", "learner-work"}
errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


def read_json(path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return None


def require_file(relative):
    path = ROOT / relative
    check(path.is_file(), f"Missing file: {relative}")
    return path


def main():
    course = read_json(ROOT / "course-map.json")
    if course is None:
        return finish()
    for key in ("entrypoint", "bridge", "calendar", "assessment", "validation"):
        require_file(course[key])
    months = course["months"]
    check([m["month"] for m in months] == list(range(1, 25)), "Months must be exactly 1-24 in order")
    weeks = [week for month in months for week in month["weeks"]]
    check([week["week"] for week in weeks] == list(range(1, 97)), "Weeks must be exactly 1-96 in order")
    counts = Counter(week["type"] for week in weeks)
    check(counts == {"build_apply": 70, "remediation": 18, "defense_transfer": 8}, f"Incorrect calendar budget: {dict(counts)}")
    check(course["schedule"]["scheduled_weeks"] == len(weeks), "Declared week budget disagrees with calendar")
    for category, count in counts.items():
        check(course["schedule"][category] == count, f"Declared {category} budget disagrees")
    gate_text = (ROOT / course["assessment"]).read_text() if (ROOT / course["assessment"]).is_file() else ""
    all_outcomes = []
    lesson_paths = []
    for month in months:
        expected_gate = f"G{(month['month'] - 1) // 6 + 1}"
        check(month["gate"] == expected_gate, f"Month {month['month']}: incorrect gate")
        check(len(month["weeks"]) == 4, f"Month {month['month']}: expected four weeks")
        check(len(month["outcomes"]) == 2, f"Month {month['month']}: expected two outcomes")
        all_outcomes.extend(month["outcomes"])
        check(month["exercise"] in gate_text, f"Exercise absent from gate rubric: {month['exercise']}")
        for outcome in month["outcomes"]:
            check(outcome in gate_text, f"Outcome absent from gate rubric: {outcome}")
        for relative in month["lessons"]:
            path = require_file(relative)
            lesson_paths.append(relative)
            if path.is_file():
                check(month["exercise"] in path.read_text(), f"{relative}: missing exercise mapping {month['exercise']}")
        expected_tracks = 2 if 8 <= month["month"] <= 12 else 1
        check(len(month["lessons"]) == expected_tracks, f"Month {month['month']}: wrong number of tracks")
    check(len(set(all_outcomes)) == 48, "Outcomes must be 48 unique IDs")
    for gate in ("G1", "G2", "G3", "G4"):
        subset = [m for m in months if m["gate"] == gate]
        check(len({m["exercise"] for m in subset}) == 6, f"{gate}: expected six unique exercises")
        check(len([o for m in subset for o in m["outcomes"]]) == 12, f"{gate}: expected twelve outcomes")
    for relative in course["specialties"]:
        require_file(relative)
    check(len(course["specialties"]) == 4, "Expected four specialty choices")
    capstones = list((ROOT / course["capstones"]).glob("*.md"))
    check(len([p for p in capstones if p.name != "README.md"]) >= 3, "Expected three role-family capstone documents")
    check(any((ROOT / "practicum/instructor").glob("*.md")), "Practicum requires separate instructor keys")

    source_ids = []
    source_count = 0
    required_fields = {"id", "title", "url", "accessed_at", "version_scope", "supports", "limitations"}
    for relative in course["source_ledgers"]:
        ledger = read_json(require_file(relative))
        if ledger is None:
            continue
        records = ledger.get("sources", []) if isinstance(ledger, dict) else ledger
        check(isinstance(records, list) and bool(records), f"{relative}: source records must be a nonempty list")
        if not isinstance(records, list):
            continue
        for record in records:
            missing = required_fields - record.keys()
            check(not missing, f"{relative}: source missing fields {sorted(missing)}")
            source_ids.append(record.get("id"))
            source_count += 1
            check(urlsplit(record.get("url", "")).scheme == "https", f"{relative}: source must have HTTPS URL")
            check(bool(re.match(r"\d{4}-\d{2}-\d{2}", record.get("accessed_at", ""))), f"{relative}: invalid source access date")
    check(len(set(source_ids)) == len(source_ids), "Source IDs must be unique across ledgers")

    markdown = [p for p in ROOT.rglob("*.md") if not EXCLUDED.intersection(p.relative_to(ROOT).parts)]
    local_links = 0
    for path in markdown:
        text = path.read_text()
        # Ignore code samples; their brackets are not navigational links.
        text = re.sub(r"(?ms)^(```|~~~).*?^\1[^\n]*$", "", text)
        for target in re.findall(r"!?\[[^\]\n]*\]\(([^\n)]+)\)", text):
            target = target.split(' "', 1)[0].strip("<>")
            if target.startswith("#") or urlsplit(target).scheme:
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            local_links += 1
            check((path.parent / target).exists(), f"{path.relative_to(ROOT)}: broken local link {target}")
    print(f"Checked {len(months)} months, {len(weeks)} weeks, {len(lesson_paths)} monthly lesson entries, 48 outcomes.")
    print(f"Checked {source_count} source records and {local_links} local links in {len(markdown)} Markdown files.")
    print("Scope: structure and local file targets only; prose, remote URLs, and hardware behavior require separate review.")
    return finish()


def finish():
    for error in errors:
        print(f"FAIL: {error}")
    if errors:
        print(f"FAILED: {len(errors)} checks")
        return 1
    print("PASS: course structure and local links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
