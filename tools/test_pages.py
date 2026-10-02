"""Verify the reading edition's content, links, track navigation, and output safety."""

import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import markdown
from mkdocs.config import load_config

import build_pages as pages
from export_wiki import EXCLUDED, Snapshot, rewrite_markdown


class Content(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.pre, self.tags, self.inside_pre = [], [], False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        if tag == "pre":
            self.inside_pre = True
            self.pre.append("")

    def handle_endtag(self, tag):
        if tag == "pre":
            self.inside_pre = False

    def handle_data(self, data):
        if self.inside_pre:
            self.pre[-1] += data


class TransformationTests(unittest.TestCase):
    def test_details_transform_preserves_fenced_and_indented_examples(self):
        source = '````html\n<details>\n```\n<details>\n````\n    <details>\n<details>\n<summary>Answer</summary>\n\n1. **Reason**\n\n</details>\n'
        actual = pages.prepare_markdown(source)
        self.assertEqual(source.rsplit("<details>", 1)[0], actual.rsplit('<details markdown="1">', 1)[0])
        self.assertEqual(1, actual.count('<details markdown="1">'))

    def test_markdown_renders_answer_lists_and_ordered_list_start(self):
        config = load_config(str(pages.ROOT / "mkdocs.yml"))
        source = '<details>\n<summary>Answer</summary>\n\n7. **First**\n8. Second\n\n</details>\n\n- Separate unordered item\n'
        body = markdown.markdown(pages.prepare_markdown(source), extensions=config.markdown_extensions, extension_configs=config.mdx_configs)
        tree = ET.fromstring("<root>" + body + "</root>")
        self.assertEqual("7", tree.find("details/ol").attrib["start"])
        self.assertEqual(2, len(tree.findall("details/ol/li")))
        self.assertEqual("First", tree.find("details/ol/li/strong").text)
        self.assertEqual(1, len(tree.findall("ul/li")))

    def test_page_links_and_source_links_preserve_fragments_and_pin_revision(self):
        snapshot = SimpleNamespace(ref="a" * 40, files={"chapter/one.md": "100644", "chapter/two.md": "100644", "data/example.json": "100644"}, directories={"chapter", "data", "."})
        links = pages.PageLinks(snapshot, {"chapter/one.md": "One", "chapter/two.md": "Two"})
        source = '[two](two.md#topic) [data](../data/example.json?raw=1) `[example](two.md)`'
        actual = rewrite_markdown(source, lambda target: links.rewrite(target, "chapter/one.md"))
        self.assertIn("[two](Two.md#topic)", actual)
        self.assertIn(f"/blob/{snapshot.ref}/data/example.json?raw=1", actual)
        self.assertIn("`[example](two.md)`", actual)
        for target in ("../learner-work/private.md", "../.cache/private.md", "../../private.md", "/Users/person/private.md", "file:///tmp/private.md"):
            with self.subTest(target=target), self.assertRaises(ValueError):
                links.rewrite(target, "chapter/one.md")

    def test_output_refuses_unmanaged_and_symlinked_directories(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            with patch.object(pages, "ROOT", root):
                output = root / ".cache/pages-docs"
                output.mkdir(parents=True)
                (output / "keep.txt").write_text("keep")
                with self.assertRaisesRegex(ValueError, "unmanaged"):
                    pages.owned_directory(output)
                self.assertEqual("keep", (output / "keep.txt").read_text())
                (output / "keep.txt").unlink()
                pages.owned_directory(output)
                (output / "outside").symlink_to(root, target_is_directory=True)
                with self.assertRaisesRegex(ValueError, "Unsafe"):
                    pages.owned_directory(output)
                with self.assertRaises(ValueError):
                    pages.owned_directory(root)


class BuiltEditionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = pages.ROOT / ".cache/pages-site"
        cls.manifest = json.loads((cls.site / pages.MANIFEST).read_text())
        cls.snapshot = Snapshot(pages.ROOT, cls.manifest["source_ref"])
        cls.rendered, cls.expected_manifest = pages.render(cls.snapshot)

    def test_complete_allowlist_and_committed_source_hashes(self):
        self.assertEqual(61, len(self.manifest["pages"]))
        self.assertEqual(30, len(set(self.manifest["teaching_chapters"])))
        self.assertEqual(self.manifest, self.expected_manifest)
        expected_files = {"index.md", "stylesheets/course.css", pages.MANIFEST} | set(self.manifest["pages"].values())
        self.assertEqual(expected_files, set(self.rendered))
        for source, digest in self.manifest["source_sha256"].items():
            with self.subTest(source=source):
                self.assertEqual(digest, hashlib.sha256(self.snapshot.read(source).encode()).hexdigest())
                self.assertFalse(EXCLUDED.intersection(Path(source).parts))
                self.assertNotIn(Path(source).parts[0], {"docs", "validation", "decisions"})

    def test_all_original_code_and_answer_containers_reach_html(self):
        details, diagrams = 0, 0
        for source, name in self.manifest["pages"].items():
            original = self.snapshot.read(source)
            html = (self.site / name.removesuffix(".md") / "index.html").read_text()
            content = Content(html)
            with self.subTest(source=source):
                self.assertEqual(original.count("<details>"), content.tags.count("details"))
                self.assertEqual(original.count("<summary>"), content.tags.count("summary"))
                blocks = re.findall(r"(?ms)^(`{3,}|~{3,})[^\n]*\n(.*?)^\1[ \t]*(?=\n|$)", original)
                self.assertEqual(len(blocks), len(content.pre))
                for (_, expected), actual in zip(blocks, content.pre):
                    self.assertEqual(expected.rstrip("\n"), actual.rstrip("\n"))
                self.assertNotIn('<details markdown="1">', html)
            details += content.tags.count("details")
            diagrams += html.count('<pre class="mermaid">')
        self.assertEqual(19, details)
        self.assertEqual(8, diagrams)

    def test_branch_navigation_does_not_require_switching_platform(self):
        month7 = self.rendered["07-Workload-Contract.md"].rsplit("\n---\n", 1)[1]
        self.assertIn("Next: Kubernetes 08", month7)
        self.assertIn("Next: Slurm 08", month7)
        for track, other in (("Kubernetes", "Slurm"), ("Slurm", "Kubernetes")):
            footer = self.rendered[track + "-12-Integration-and-Comparison.md"].rsplit("\n---\n", 1)[1]
            self.assertIn(f"Previous: {track} 11", footer)
            self.assertIn("Next: 13 Fleet Truth", footer)
            self.assertNotIn(f"Next: {other}", footer)
            html = (self.site / (track + "-12-Integration-and-Comparison") / "index.html").read_text()
            self.assertIn('<link rel="next" href="../13-Fleet-Truth/">', html)
        config = load_config(str(pages.ROOT / "mkdocs.yml"))
        self.assertNotIn("navigation.footer", config.theme["features"])
        self.assertEqual("", config.edit_uri)

    def test_every_built_local_link_and_anchor_resolves_under_pages_basepath(self):
        self.assertGreater(pages.validate_site(self.site, self.manifest), 1000)

    def test_html_checker_rejects_broken_raw_html_links_and_anchors(self):
        with tempfile.TemporaryDirectory() as temporary:
            site = Path(temporary)
            (site / "404.html").write_text("<h1>Missing</h1>")
            for target in ("/escape/", "Missing/", "#missing"):
                (site / "index.html").write_text(f'<a href="{target}">Bad</a>')
                with self.subTest(target=target), self.assertRaisesRegex(ValueError, "Link escapes|Missing built"):
                    pages.validate_site(site, {"pages": {}})

    def test_homepage_links_are_rendered_and_search_covers_both_tracks(self):
        home = (self.site / "index.html").read_text()
        self.assertIsNone(re.search(r"\[[^\]\n]+\]\([^\)\n]*\.md[^\)\n]*\)", home), "Homepage contains an unrendered Markdown link")
        self.assertIsNone(re.search(r"\{\{[^}]+\}\}", home), "Homepage contains an unresolved placeholder")
        search = json.loads((self.site / "search/search_index.json").read_text())
        locations = {entry["location"].split("#")[0] for entry in search["docs"]}
        self.assertTrue({"Kubernetes-Track/", "Slurm-Track/", "01-System-Map/"} <= locations)


if __name__ == "__main__":
    unittest.main()
