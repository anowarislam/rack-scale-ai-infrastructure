# Month 23: make one portfolio decision and follow it through

**G4-E05: G4-O09 and G4-O10.** Deliver your selected [role-family capstone](capstones/README.md), then update it under changed evidence. The role changes the decision you own, not the standard of truth.

## From a technical finding to an operating choice

A portfolio decision allocates scarce capacity, money, time, or risk across competing work. It names the binding constraint and what will not be done. A list of desirable initiatives is not a decision. Neither is a numerical ranking whose precision exceeds its evidence.

**Worked example 1.** A team has ten discretionary hours. A monitoring fix needs six, a required compatibility investigation needs five, and an optimization needs eight. All three cannot fit. If readiness depends on compatibility, selecting monitoring plus optimization while calling compatibility critical is inconsistent. One defensible choice is five hours of compatibility and five of monitoring, with completion next week. Another is monitoring now and an explicit launch hold. The dependency determines the choice.

**Worked example 2.** A rack costs 100 synthetic budget units and arrives in six weeks. A gap begins tomorrow. It may be the right six-week investment but cannot resolve tomorrow's shortage. Pair it with a bounded demand reduction, rescheduling, or already qualified capacity. Give the temporary arrangement an owner and expiry.

**Counterexample.** Multiplying an unmeasured outage probability by a precise-looking loss estimate can create a false expected-value ranking. Label the probability as a scenario assumption and test whether the decision changes across plausible values.

## Student brief

Meridian has 128 installed GPUs in four domains. Its previously justified commitment is 72 GPUs under the exercise loss/headroom model. Product asks for 96 in two weeks. A rack may be unavailable for qualification during that window. Six assets await repair; five enter and three return qualified each week under the current synthetic flow. There are 12 discretionary engineering hours this week.

Choose one capstone role and one main decision. The engineer may reduce recurrence in qualification/recovery. The aspiring leader may coordinate readiness and closure. The manager may choose the demand/capacity/risk portfolio. All must account for the same constraints.

| Option | Given scope | Limitation |
|---|---|---|
| Buy one qualified 32-GPU domain | 100 synthetic budget units; six-week lead time | Not available in the two-week window |
| Reschedule up to 24 GPUs of deferrable work | Requires product agreement; expires after two weeks | Creates later backlog/fairness cost |
| Improve repair handoff | 8h; pilot suggests two additional returns/week | Small pilot, not guaranteed capacity |
| Complete compatibility evidence | 6h for one bounded test | May discover a blocker |

You may defend another bounded choice. Do not assume pilot effects or stakeholder agreements are confirmed. The [key](instructor/23-key.md) releases changes in two sessions separated by a learner work cycle.

## Decide, execute, and revisit

Session 1: present a one-page decision with alternatives, dependency map, capacity calculation, owner roles, deadlines, and residual risks. Delegate two bounded items with acceptance criteria. The observer records whether the delegate understood the expected result and escalation boundary.

Between sessions, perform the local analysis, validation, or artifact improvement your decision requires. This is real course work, not authorization to contact actual stakeholders. Session 2 supplies outcomes from simulated external owners. Reconcile them with completed work; revise your decision when warranted. Show one closed acceptance condition and one open item.

Integrate your specialty evidence. A proposed fix alone is not a completed intervention. Retain failed experiments and explain their effect on priority. Finish with a 150-word executive note stating decision, reason, consequence, and next review trigger.

## Assessment and scope

The common rubric evaluates technical grounding, choice under constraints, delegation clarity, changed-evidence response, and closure. The capstone packet adds role criteria and exemplar fragments. The observer scores behavior actually seen; polished documents do not prove influence or sustained management.

Two course cycles may establish course-observed planning and follow-through. They do not establish long-term coaching, succession, organization health, or director job equivalence. Workplace evidence must be separately labeled and permissioned.

Abort actual infrastructure, procurement, or external-message actions. This exercise changes local artifacts only. Reset by restoring the initial scenario ledger while retaining both decision versions. Objective checks focus on coherent arithmetic, dependency-aware choice, explicit tradeoffs, evidence-backed revision, and closed acceptance conditions, not a mandatory spending answer.

## Questions

1. Which option could help the two-week gap, and what does it depend on?
2. Why keep the repair pilot separate from committed capacity?
3. What demonstrates delegation beyond assigning a task?
4. Which new observation would reverse your recommendation?

## Four defense and transfer weeks

At 9h/week: week 1 selects and defends the decision; week 2 executes bounded work and records delegation; week 3 integrates follow-up evidence and closure; week 4 prepares the role-family defense. These are reserved defense/transfer weeks. Continue to [Month 24](24-defense.md).
