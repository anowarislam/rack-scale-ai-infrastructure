# Publish the course reading edition

Edit lessons in the source repository, commit the change, and regenerate the wiki from that commit. The wiki is a reading edition; executable code, fixtures, source ledgers, validation reports, and project history remain in the repository. GitHub Wiki uses its own Git repository.

The exporter uses Python 3.11 or later and the standard library. It reads committed Git objects, so uncommitted lesson edits are not included. Its explicit allowlist exports 61 source documents: all 30 teaching chapters, the learner guides, track indexes, assessments, specialties, practicum and instructor keys, practical instructions, and evidence introduction. It also generates `Home.md`, `_Sidebar.md`, and `_Footer.md`.

## Generate and verify

Run from the course repository root, after committing the source changes:

```bash
python3 -m unittest discover -s tools -p 'test_export_wiki.py' -v
python3 tools/validate_course.py
python3 tools/export_wiki.py --source-ref HEAD
python3 tools/export_wiki.py --source-ref HEAD --check
```

The output is `.cache/wiki-export/`. For a different staging name, pass `--output .cache/wiki-export-review`. Output must be below this repository's `.cache`; the tool refuses the cache root, path traversal, and symlinked staging paths. It refuses to overwrite an unmanaged nonempty directory, unknown files, or generated pages that were edited after export. Resolve those differences explicitly or use a new empty staging directory.

The exact commit appears in the command output, the wiki footer, and `wiki-export-manifest.json`. The manifest maps each source file to its wiki filename and records a SHA-256 hash for every generated Markdown file. It is staging metadata, not a wiki page. Identical source and exporter versions produce identical file contents. `--check` validates that the existing export matches the requested revision without writing files.

Open `Home.md`, `_Sidebar.md`, a chapter from each platform track, and a practicum key. Verify the intended reading route before publication. The keys are intentionally public and sealed only by convention; a learner should attempt a scenario before opening its key.

## Publish through the separate wiki repository

GitHub requires the first wiki page to be created in the repository's Wiki UI before the wiki Git repository can be cloned. The source repository's wiki must be enabled. Once initialized, clone its separate remote:

```bash
git clone https://github.com/anowarislam/rack-scale-ai-infrastructure.wiki.git .cache/wiki-repo
```

Keep `.cache/wiki-repo` separate from the export directory. Review the wiki's existing files and Git status first. Apply only Markdown files named in the manifest's `files` map. Do not copy the manifest, delete arbitrary wiki pages, or run a whole-directory mirror. On a first publication, the initial UI-created `Home.md` must be reviewed and intentionally replaced by the generated course home.

For later publication, retain the prior export manifest outside the wiki repository. Compare its filenames and hashes with the current wiki checkout before replacing or removing a generated page. If an existing page differs from the prior generated hash, reconcile the edit in the source repository or preserve it deliberately. The exporter protects its staging directory; it does not apply changes to, or police concurrent edits in, the wiki repository.

After copying the reviewed pages, inspect `git diff --check` and `git diff --stat` in the wiki checkout, then commit and push the wiki's default branch with a normal fast-forward push. GitHub publishes only that branch. The initial wiki for this repository uses `master`; verify the remote default before a later publication. A push rejection requires fetching and reconciling concurrent changes, not a force push. The source repository commit and wiki commit are separate operations. Record both commit hashes in the publication result. The exporter never commits, pushes, or changes repository settings.

Finally, open the public wiki home, follow a chapter link, follow both platform routes, and test a source-code link. Confirm that the page displays the intended source commit. Local export checks do not establish that a remote push succeeded or that GitHub rendered the pages correctly.

## Link and content behavior

- Exported Markdown links become absolute links to their stable wiki page names. Month navigation preserves the Kubernetes and Slurm branches and reunites them at month 13.
- Relative links to other tracked files or directories become `blob` or `tree` links pinned to the full source commit. Untracked, missing, private-output, and repository-escaping links fail the export.
- External URLs, local heading anchors, query strings, link titles, and reference-style links are retained. Paths containing spaces and parentheses are supported.
- Fenced code, Mermaid blocks, inline code, indented code, and answer-detail containers are preserved. The exporter changes Markdown navigation destinations and appends course navigation; it does not translate commands into wiki paths.
- Historical administration and validation reports are linked to their source snapshot rather than copied into current wiki claims. The home page is generated independently of the source README's publication status.

The parser targets the course's Markdown link syntax; it is not a general Markdown renderer. Raw HTML URL attributes and arbitrary wiki-link syntax are not converted. The checks verify local targets and export integrity, not external site availability, teaching quality, physical lab behavior, or learner mastery.

GitHub documents [adding and editing wiki pages](https://docs.github.com/en/communities/documenting-your-project-with-wikis/adding-or-editing-wiki-pages) and [creating a wiki footer or sidebar](https://docs.github.com/en/communities/documenting-your-project-with-wikis/creating-a-footer-or-sidebar-for-your-wiki). Wiki filenames determine page titles; `_Sidebar.md` and `_Footer.md` supply the shared navigation.
