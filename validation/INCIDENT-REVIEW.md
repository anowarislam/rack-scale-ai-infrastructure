# Failure casebook acceptance record

Review date: 2026-10-02. Scope: the new `incidents/` section, its three primary-source ledgers, and its integration into the existing course website. The purpose is to teach mechanisms and operational reasoning through public failure accounts, with theory and examples before exercises.

## Content delivered

The section contains 13 cases: 11 incident reviews and two explicitly labeled fleet studies. A reading method, index, and review workshop bring the addition to 16 pages. There are 15 answer disclosures and five original Mermaid diagrams in the addition. Every case includes a published account, a synthetic worked example, a decision question with reasoning, transfer to AI infrastructure, and evidence limits.

Mechanisms include network and control-plane dependencies, state divergence, algorithmic resource exhaustion, latent software defects, scale-dependent observation costs, destructive operation scope, backup validity, physical common causes, training interruptions, silent corruption, repair amplification, maintenance authority, and data isolation. The section does not claim to cover every failure mechanism or estimate their prevalence.

The three added ledgers contain 13 records, bringing the course to 107 source records. Public reports substantiate attributed historical claims. They do not establish independent access to private logs, present-day vendor architecture, or measurements from the learner's fleet.

## Review and corrections

Three GPT Astra agents at maximum reasoning effort researched and authored separate groups. The network/software and recovery/isolation authors cross-reviewed each other's cases against the primary sources. The coordinator independently reviewed the four hardware/fleet cases and recomputed their examples. The hardware/fleet author reviewed the coordinator's reading method, index, workshop, and publication-code changes.

Corrections and boundaries retained in the delivered content:

- Fastly's 10:27 timestamp denotes identification of the relevant configuration; disablement is described subsequently without assigning it that exact time.
- Operator-reported corrective actions are distinguished from planned changes and original course recommendations.
- The Llama v3 paper's faulty-GPU row shows a count and percentage that do not agree. The case identifies the discrepancy without inventing a corrected classification or a per-device failure rate.
- Google's network incident page has differing summary and detailed timing statements. The case uses the detailed report's region-dependent duration and does not invent a universal restoration time.
- Cloudflare's power report labels parts of the provider's electrical sequence as speculation. That uncertainty remains explicit.
- GitHub's recovery account does not justify a blanket claim that all state and queued side effects recovered losslessly.
- The OpenAI control-plane case does not generalize its reported service-discovery dependencies to all Kubernetes deployments.

Independent numerical checks covered common-cause probability, queue growth and drain, failure-domain capacity, recovery deadlines, checkpoint overhead, bounded matching work, replica disagreement, storage repair capacity, weighted correctness checks, and data-isolation validation. These are checks of the stated teaching models, not reproductions of production events.

## Validation scope

Before release, the course validator passed schedule accounting, the 48 outcome mappings, all 107 source-record structures, and local Markdown file targets. All 16 added Markdown pages rendered with the pinned site extensions and passed ASCII, single-title, and answer-container checks. The existing five exercise suites passed all 57 tests. The four site transformation tests also passed during independent review.

The website allowlist now contains 77 source pages plus the homepage; all 30 core teaching chapters remain included. The historical wiki allowlist is separate. Added site checks require every case to have source evidence, a rendered answer, and a search-index entry. Existing site checks validate committed source hashes, code preservation, answer containers, internal HTML links and anchors, and platform-track navigation.

For release-specific build and deployment evidence, use the [Pages workflow runs](https://github.com/anowarislam/rack-scale-ai-infrastructure/actions/workflows/pages.yml) for the source revision identified by the live website's `course-manifest.json`. A source review or successful push alone is not proof of publication. The [publishing procedure](../docs/pages-publishing.md) describes the strict build, site tests, and live browser checks.

No historical incident was reproduced against a live service. No native-platform or physical-hardware acceptance claim changes. Reading the cases does not establish learner mastery or production incident leadership.
