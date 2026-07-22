---
name: review
description: >
  Stage 7 of the paper pipeline: simulate program-committee peer review with
  three reviewer subagents, then revise and re-review until every reviewer
  is at accept or better. Use after the draft is approved, or any time the
  user asks for a mock review of a manuscript.
---

# Stage 7 — Review loop

Goal: the manuscript survives a simulated program committee. Loop:
review → respond → revise → re-review, until all three reviewers score
**accept or better**, then close at gate G6.

## Round structure

### 0. Claim–citation audit (round 1, and any round where refs.bib changed)

Before the reviewers see the manuscript, audit whether the cited sources
actually say what the paper claims they say:

1. List every citation-anchored claim in the manuscript. Mark as
   **high-impact** any claim that carries a number taken from the cited
   work, a causal or conclusion-level statement, or a "first/only/best"
   positioning; the rest are routine.
2. Verify all high-impact claims, plus a ~10% sample of the routine ones
   (at least 3, or all if fewer): fetch the cited source (the `pdf` link
   from `scholar_search`, or the arXiv page) and check that it supports
   the sentence as written.
3. Verdict per claim: **supported** / **distorted** (source says something
   weaker or different) / **unsupported** (source does not contain it) /
   **unverifiable** (source unreachable — say why).

Store the audit as `paper/reviews/round-N/citation-audit.md`. Distorted and
unsupported claims are must-fix before the round proceeds — fix the text or
the citation, never the audit. An unverifiable high-impact claim goes to
the user with a recommendation.

### 1. Spawn three reviewers

Launch three parallel `reviewer` subagents against the current PDF/source,
each with a distinct persona (pass persona + venue + manuscript path in the
prompt):

- **Reviewer A — domain expert.** Knows the closest prior work intimately;
  expertise 4/4. Hunts: missing citations, overlap with prior systems,
  overclaimed novelty, whether the key idea is actually new.
- **Reviewer B — methods hawk.** Cares about experimental rigor; hunts:
  missing baselines, unfair tuning, no error bars, cherry-picked workloads,
  claims the evaluation doesn't test, statistical sloppiness.
- **Reviewer C — informed outsider.** Adjacent area, expertise 2/4; reads
  like a busy PC member with 15 papers in the stack. Hunts: unclear writing,
  undefined terms, unmotivated design, "why should I care", whether the
  intro's promises survive the details.

Store each review as `paper/reviews/round-N/reviewer-{A,B,C}.md`.

### 2. Triage the reviews

Merge all points into a single numbered list in
`round-N/response.md`, classified:

- **Must fix** — soundness problems, missing experiments/baselines, missing
  key citations. These may send the pipeline back to Stages 3–5; that is the
  loop working as designed, not a failure. New experiments mean real runs —
  the integrity rule applies inside the review loop too.
- **Should fix** — clarity, structure, positioning, presentation.
- **Contest** — points where the reviewer is wrong. Rare, and per SPJ still
  your fault: if a competent reviewer misread it, the paper misled them.
  Fix the text so the misreading is impossible, then note the disagreement.

Never ignore a point silently. If a demanded change is out of scope or would
need resources you don't have, take it to the user with a recommendation.

### 3. Revise

Apply fixes (re-entering earlier stage skills as needed), recompile, and
record in `response.md` what changed for each numbered point — the same
discipline as a real rebuttal plus revision.

### 4. Re-review

First close the response ledger: mark every numbered point in `response.md`
as **fulfilled**, **partial**, **not-fulfilled**, or **contested** (with
the rationale from triage). A partial or not-fulfilled point without a
recorded reason carries into the next round as an automatic must-fix — a
promise in a response is a debt, not an answer.

Then the next round: if the revision touched `refs.bib`, re-run the
claim–citation audit (step 0) first. Spawn the same three personas, given
the revised manuscript **and** the previous round's reviews plus
`response.md` with its ledger, instructed to verify whether each of their
points was addressed and to score afresh.

## Termination

- **Success:** all three reviewers at accept or better → gate G6.
- **Stall:** a reviewer repeats the same must-fix two rounds in a row, or
  4 rounds elapse without convergence → stop looping and take stock with the
  user: the sticking points, what fixing them would cost, and your
  recommendation (fix, reframe the claims, or target a different venue).
  Endless polishing loops burn effort without adding substance.

## Gate G6

Report to the user: rounds taken, final scores, what changed since their
approved draft, and any contested points. On sign-off, proceed to finalize.
