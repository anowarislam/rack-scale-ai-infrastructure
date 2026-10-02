"""Behavioral checks for the reading edition; no network or wiki writes."""

import hashlib
import json
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest

import export_wiki as wiki


class LinkTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = SimpleNamespace(
            ref="a" * 40,
            files={path: "100644" for path in (
                "curriculum/lesson.md", "curriculum/next.md", "fixtures/data.json",
                "fixtures/data set.json", "fixtures/a(b).json", "validation/RESULTS.md",
            )},
            directories={".", "fixtures", "curriculum", "validation"},
        )
        self.links = wiki.Links(self.snapshot, {"curriculum/next.md": "Next-Lesson"})

    def rewrite(self, text):
        return wiki.rewrite_markdown(text, lambda target: self.links.rewrite(target, "curriculum/lesson.md"))

    def test_pages_files_directories_queries_and_fragments(self):
        source = '[next](next.md#why) [data](../fixtures/data.json?raw=1#L2) [dir](../fixtures/) [report](../validation/RESULTS.md)'
        actual = self.rewrite(source)
        self.assertIn(f"[next]({wiki.REPOSITORY}/wiki/Next-Lesson#why)", actual)
        self.assertIn(f"[data]({wiki.REPOSITORY}/blob/{self.snapshot.ref}/fixtures/data.json?raw=1#L2)", actual)
        self.assertIn(f"[dir]({wiki.REPOSITORY}/tree/{self.snapshot.ref}/fixtures)", actual)
        self.assertIn(f"[report]({wiki.REPOSITORY}/blob/{self.snapshot.ref}/validation/RESULTS.md)", actual)

    def test_titles_spaces_parentheses_and_references(self):
        source = '''[A](<../fixtures/data set.json> "A title")
[B](../fixtures/a(b).json 'B title')
[C](../fixtures/a\\(b\\).json)
[D][lesson]
[lesson]: next.md#topic "Reference title"
'''
        actual = self.rewrite(source)
        self.assertIn('fixtures/data%20set.json> "A title"', actual)
        self.assertIn("fixtures/a%28b%29.json 'B title'", actual)
        self.assertIn("fixtures/a%28b%29.json)", actual)
        self.assertIn(f'[lesson]: {wiki.REPOSITORY}/wiki/Next-Lesson#topic "Reference title"', actual)
        self.assertIn("[D][lesson]", actual)

    def test_external_links_and_local_anchors_are_unchanged(self):
        source = '[web](https://example.org/a(b)?q=x#part) [mail](mailto:a@example.org) [cdn](//example.org/a) [here](#heading)'
        self.assertEqual(source, self.rewrite(source))

    def test_code_examples_mermaid_and_details_are_preserved(self):
        protected = '''`[inline](next.md)` and ``a `[inline](next.md)` b``
````markdown
[example](next.md)
```
[still example](next.md)
````
~~~mermaid
flowchart LR
  A["[node](next.md)"] --> B
~~~
    [indented](next.md)
'''
        self.assertEqual(protected, self.rewrite(protected))
        actual = self.rewrite(protected + '\n<details>\n<summary>Answer</summary>\n\n[read](next.md)\n\n</details>\n')
        self.assertTrue(actual.startswith(protected))
        self.assertIn(f"[read]({wiki.REPOSITORY}/wiki/Next-Lesson)", actual)
        self.assertIn("<summary>Answer</summary>", actual)
        self.assertTrue(actual.endswith("</details>\n"))

    def test_unknown_private_and_outside_paths_are_rejected(self):
        for target in ("missing.md", "../../outside.md", "../.cache/secret.md", "../learner-work/private.md", "/Users/author/private.md", "file:///tmp/private.md"):
            with self.subTest(target=target), self.assertRaises(ValueError):
                self.rewrite(f"[unsafe]({target})")

    def test_collisions_and_unsafe_allowlist_entries_are_rejected(self):
        for specs in (
            (("a.md", "Lesson"), ("b.md", "lesson")),
            (("a.md", "Lesson"), ("a.md", "Other")),
            (("a.md", "Home"),), (("../a.md", "Lesson"),),
            ((".cache/a.md", "Lesson"),), (("a.md", "../Lesson"),),
        ):
            with self.subTest(specs=specs), self.assertRaises(ValueError):
                wiki.page_map(specs)

    def test_exported_link_target_validation(self):
        wiki.validate_links({"Next-Lesson.md": "# Next\n", "Home.md": f"[next]({self.links.wiki}Next-Lesson)"}, self.links)
        for target in (self.links.wiki + "Missing", "next.md", "file:///tmp/secret"):
            with self.subTest(target=target), self.assertRaises(ValueError):
                wiki.validate_links({"Home.md": f"[bad]({target})"}, self.links)


class OutputSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.output = self.root / ".cache/wiki-export"
        self.rendered = {"Home.md": "# Course\n"}
        self.manifest = wiki.export_manifest(self.rendered, {}, SimpleNamespace(ref="a" * 40))

    def write(self, check=False):
        return wiki.write_export(self.root, self.output, self.rendered, self.manifest, check)

    def test_deterministic_rerender_and_check(self):
        self.write()
        before = {p.name: p.read_bytes() for p in self.output.iterdir()}
        self.write()
        self.write(check=True)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.output.iterdir()})
        self.manifest["source_ref"] = "b" * 40
        with self.assertRaisesRegex(ValueError, "does not match"):
            self.write(check=True)

    def test_unmanaged_directory_is_not_overwritten(self):
        self.output.mkdir(parents=True)
        (self.output / "Home.md").write_text("An existing wiki page")
        with self.assertRaisesRegex(ValueError, "not a managed export"):
            self.write()
        self.assertEqual("An existing wiki page", (self.output / "Home.md").read_text())

    def test_unknown_and_edited_files_are_not_overwritten(self):
        self.write()
        unknown = self.output / "Unowned.md"
        unknown.write_text("Keep this")
        with self.assertRaisesRegex(ValueError, "unowned"):
            self.write()
        self.assertEqual("Keep this", unknown.read_text())
        unknown.unlink()
        (self.output / "Home.md").write_text("Manual correction")
        with self.assertRaisesRegex(ValueError, "edited or is unsafe"):
            self.write()
        self.assertEqual("Manual correction", (self.output / "Home.md").read_text())

    def test_paths_outside_staging_and_symlinks_are_rejected(self):
        for output in (self.root, self.root / ".cache", self.root / ".cache/../source", self.root / "wiki"):
            with self.subTest(output=output), self.assertRaises(ValueError):
                wiki.write_export(self.root, output, self.rendered, self.manifest)
        self.output.parent.mkdir()
        self.output.symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlinked"):
            self.write()

    def test_only_previously_owned_stale_pages_are_removed(self):
        self.rendered["Old.md"] = "# Old\n"
        self.manifest = wiki.export_manifest(self.rendered, {}, SimpleNamespace(ref="a" * 40))
        self.write()
        del self.rendered["Old.md"]
        self.manifest = wiki.export_manifest(self.rendered, {}, SimpleNamespace(ref="b" * 40))
        self.write()
        self.assertFalse((self.output / "Old.md").exists())
        self.assertTrue((self.output / "Home.md").is_file())


class CourseExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snapshot = wiki.Snapshot(wiki.ROOT, "HEAD")
        cls.rendered, cls.pages = wiki.render(cls.snapshot)

    def test_full_chapter_coverage_and_only_explicit_tracked_sources(self):
        course = json.loads(self.snapshot.read("course-map.json"))
        chapters = {course["bridge"]} | {p for m in course["months"] for p in m["lessons"]}
        self.assertEqual(30, len(chapters))
        self.assertTrue(chapters <= self.pages.keys())
        self.assertEqual(61, len(self.pages))
        self.assertEqual(64, len(self.rendered))
        self.assertTrue(set(self.pages) <= self.snapshot.files.keys())
        for source in self.pages:
            self.assertFalse(wiki.EXCLUDED.intersection(Path(source).parts))
            self.assertNotIn(source, {"README.md", "DELIVERY-STATUS.md", "course-charter.md"})
            self.assertNotIn(source.split("/")[0], {"validation", "decisions", "docs"})
            self.assertIn(self.pages[source], self.rendered["Home.md"])

    def test_all_original_fences_and_answer_containers_survive(self):
        for source, name in self.pages.items():
            original = self.snapshot.read(source)
            actual = self.rendered[name + ".md"]
            for block in re.finditer(r"(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1[ \t]*(?=\n|$)", original):
                with self.subTest(source=source):
                    self.assertIn(block[0], actual)
            for tag in ("<details>", "</details>", "<summary>", "</summary>"):
                self.assertEqual(original.count(tag), actual.count(tag), source)
            self.assertNotRegex(actual, r"/Users/|/home/[^ /]+/")

    def test_branch_navigation_and_source_pinning(self):
        month7 = self.rendered["07-Workload-Contract.md"]
        self.assertIn("Next: Kubernetes 08 Reference Environment", month7)
        self.assertIn("Next: Slurm 08 Reference Environment", month7)
        kube9 = self.rendered["Kubernetes-09-Placement-and-Fairness.md"]
        self.assertIn("Previous: Kubernetes 08 Reference Environment", kube9)
        self.assertIn("Next: Kubernetes 10 Workload Recovery", kube9)
        self.assertNotIn("Next: Slurm", kube9)
        self.assertIn("Previous: Kubernetes 12", self.rendered["13-Fleet-Truth.md"])
        self.assertIn("Previous: Slurm 12", self.rendered["13-Fleet-Truth.md"])
        self.assertIn(f"/blob/{self.snapshot.ref}/evidence/systems-sources.json", self.rendered["Sources-and-Evidence.md"])
        self.assertIn(f"git checkout {self.snapshot.ref}", self.rendered["Home.md"])
        wiki.validate_links(self.rendered, wiki.Links(self.snapshot, self.pages))

    def test_manifest_hashes_match_generated_bytes(self):
        manifest = wiki.export_manifest(self.rendered, self.pages, self.snapshot)
        self.assertEqual(set(self.rendered), set(manifest["files"]))
        for name, body in self.rendered.items():
            self.assertEqual(hashlib.sha256(body.encode()).hexdigest(), manifest["files"][name])
        self.assertEqual(set(self.pages), set(manifest["pages"]))


if __name__ == "__main__":
    unittest.main()
