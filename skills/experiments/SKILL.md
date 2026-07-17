---
name: experiments
description: >
  Stage 4 of the paper pipeline: run the experiments from the plan, with full
  provenance per run, and collect real data into paper/experiments/. Use
  after implementation is accepted, or when the review loop demands new
  experiments.
---

# Stage 4 — Experiments

Goal: every RQ in `paper/plan.md` answered with real, reproducible data under
`paper/experiments/`, summarized in `results.md`.

## Integrity — read first

**Every number in the paper traces to a file in this directory.** No result
may be estimated, extrapolated, interpolated from a partial run, or copied
from a prior paper as if it were measured here. If a run failed, it is a
failed run — rerun it or report the gap. This rule has no exceptions and no
user override.

## Provenance per run

One directory per run (or per sweep), self-describing:

```
experiments/
├── 01-e2e-throughput/
│   ├── run.sh              # exactly how it was launched
│   ├── config.json         # parameters, seed, workload
│   ├── env.txt             # host, commit hash of src/, versions (capture automatically)
│   ├── raw/                # untouched tool output
│   └── data.csv            # parsed, one row per measurement
└── results.md
```

- Capture `env.txt` automatically in `run.sh` — `hostname`, `git -C src rev-parse HEAD`,
  relevant `--version`s. Provenance written by hand gets forgotten.
- **Never edit raw output.** Parsing produces new files next to it.
- Repeat runs per the rigor budget in plan.md (≥5 for perf, ≥3 seeds for ML).
  Discard warm-up iterations explicitly and note that you did.

## Execution

- Respect the permission boundaries from setup (machines, budgets, quotas).
  If an experiment needs something outside them, stop and ask.
- Long jobs: run in the background with checkpoints; verify the first minutes
  of output before walking away from hours of compute.
- Watch for invalid runs, not just failed ones: a baseline misconfigured, a
  CPU governor left in powersave, a dataset partially cached. When a number
  looks too good or too bad, treat it as a bug in the harness until proven
  otherwise.

## results.md

For each RQ: which run directories answer it, the headline numbers with
variance, and a one-sentence takeaway. Then an honest overall read:

- Which contribution claims are now supported, and how strongly.
- Which are **not** supported. Do not soften this. Per the orchestrator,
  unsupported claims go back to the user: shrink the claim or loop back to
  strengthen the system.

## Gate G4

Walk the user through results.md — supported claims, unsupported claims,
surprises. The user decides: proceed to analysis/writing, or loop back.
Record the decision in STATE.md.
