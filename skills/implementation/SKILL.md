---
name: implementation
description: >
  Stage 3 of the paper pipeline: build the system or method described in the
  proposal, to the standard the experiment plan requires. Use after setup is
  approved, or when the review loop demands implementation changes.
---

# Stage 3 — Implementation

Goal: a working artifact in `paper/src/` (or the location recorded in
plan.md) that can run every experiment in the plan.

## Build discipline

- **The plan is the spec.** Before writing code, list what each RQ needs the
  artifact to do (interfaces, knobs for ablations, instrumentation points).
  Ablations in particular must be designed in: each novel component needs a
  switch to disable or replace it.
- **Instrument from day one.** Experiments need machine-readable output
  (CSV/JSON lines with config, seed, and metrics), not log scraping.
  A run that cannot be parsed is a run that gets repeated.
- **Baselines are part of the artifact.** Fetch and build the baseline
  systems now; getting a competitor's code running is routinely the slowest,
  flakiest part of a paper. Tune them fairly and record how.
- **Version everything.** Commit at meaningful checkpoints. Experiment
  provenance (Stage 4) records the commit hash of the code that produced
  each result.
- Write tests for correctness-critical pieces — a paper retracted over a
  bug in the measurement harness is the nightmare scenario.

## Keep notes for the Implementation section

Maintain `paper/src/IMPLEMENTATION_NOTES.md` as you go: languages, rough
LOC, key libraries, and the 2–3 engineering decisions that were genuinely
hard or interesting. The paper's Implementation section (~0.5–1 page) is
written from this file, and reconstructing it later from memory loses the
details reviewers like.

## Smoke experiment

Before declaring the stage done, run one miniature end-to-end experiment:
smallest workload, one seed, our system plus one baseline, through the real
measurement harness into the real output format. This shakes out the harness
while the stakes are low.

## Gate G3

Show the user: what was built, how to run it, smoke-experiment output, and
any deviation from the plan (with your reasoning). On acceptance, update
STATE.md and move to experiments.
