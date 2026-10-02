# Publish the course website

The course website is [Rack-scale AI infrastructure](https://anowarislam.github.io/rack-scale-ai-infrastructure/). GitHub Pages is the primary reading edition. The repository holds the canonical lessons, runnable exercises, source records, and validation evidence.

The user clarified that the requested destination was GitHub Pages after the first wiki publication. The website replaces the wiki as the main reading entrypoint. The wiki workflow remains available as historical tooling; updating it is not required to publish the website.

## Preview and validate

Use Python 3.12 and run from the repository root:

```bash
python3 -m venv .cache/pages-venv
.cache/pages-venv/bin/python -m pip install -r requirements-pages.txt
.cache/pages-venv/bin/python tools/validate_course.py
.cache/pages-venv/bin/python tools/build_pages.py --source-ref HEAD
.cache/pages-venv/bin/python -m unittest discover -s tools -p 'test_pages.py' -v
```

The builder stages the explicitly selected course documents in `.cache/pages-docs` and writes the website to `.cache/pages-site`. Lesson content comes from the specified Git commit; commit lesson edits before building a new edition. Site presentation files are in `site_src/`, and the MkDocs configuration is `mkdocs.yml`. Generated files and local learner work stay out of the source commit.

For a local browser preview after building:

```bash
.cache/pages-venv/bin/python -m mkdocs serve
```

Open the address printed by MkDocs, including the `/rack-scale-ai-infrastructure/` path. Re-run the builder when changing lesson content. Check the home page, a long chapter, both platform routes, search, answer disclosures, Mermaid diagrams, and mobile navigation.

## Publish

[The Pages workflow](../.github/workflows/pages.yml) runs after a push to `main` or a manual dispatch from `main`. It validates the course, builds and tests the site, uploads only `.cache/pages-site`, and deploys that artifact through GitHub Pages. The repository's Pages build source must be **GitHub Actions**.

The build job can read the source and Pages metadata. Only the deploy job receives `pages: write` and `id-token: write`. Action references and direct Python dependencies are pinned. Only one publication runs at a time; a running publication is allowed to finish.

A successful Git push is not publication evidence. Confirm the workflow's deployment succeeds, then open the public site and check its source edition, navigation, search, diagrams, answers, and a source-file link. Record the deployed source commit and workflow run URL. If a build fails, inspect its log and fix the source; the previous published site remains the available edition.

## Content and maintenance

The website includes the complete teaching route and supporting learner pages. Links between lessons stay within the website. Links to runnable files and source records identify the matching repository commit, so commands and reading material can be used together.

Change lessons in their existing source directories. Change the home page and visual styling in `site_src/`. Preserve the course's distinction between explanations, synthetic examples, executed local checks, native hardware evidence, and learner assessment.

GitHub documents the [Pages workflow and artifact deployment model](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages). MkDocs documents [configuration and site URLs](https://www.mkdocs.org/user-guide/configuration/).
