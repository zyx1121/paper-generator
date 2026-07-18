---
name: setup
description: >
  Stage 2 of the paper pipeline: choose the target venue, scaffold the paper
  workspace and LaTeX template, obtain experiment-environment access from the
  user, and write the experiment plan (research questions, baselines,
  metrics). Use after the proposal is approved.
---

# Stage 2 — Setup

Goal: everything the autonomous stages need — venue decision, workspace,
environment access, and an experiment plan — approved at gate G2.

## 1. Venue

Propose 2–3 candidate venues that fit the work's community and maturity, each
with the facts that matter, and recommend one:

- format: template (acmart sigconf / IEEEtran / usenix / neurips-style),
  page limit and whether references count, single/double column;
- review model: double-blind? rebuttal phase? artifact evaluation?
- timing: next deadline vs. realistic completion date;
- fit: where the closest prior work was published is the strongest signal.

Once the user picks, write `paper/venue.md` with the chosen venue's format
facts and submission rules (anonymization requirements included — they shape
the manuscript from day one). If the venue is double-blind, the manuscript is
anonymous from the first draft.

## 2. Workspace and template

- Create the `paper/` layout from the orchestrator skill.
- Set up `paper/manuscript/` with the venue's LaTeX class/style file
  (download the official template), a `main.tex` split into
  `sections/*.tex`, an empty `refs.bib`, and standard packages:
  `booktabs`, `subcaption`, `hyperref` then `cleveref`, `graphicx`.
- Verify the toolchain immediately: run `latex_compile` on the skeleton.
  If no LaTeX toolchain exists on this machine, tell the user what to install
  (TeX Live + latexmk, or tectonic) before proceeding.

## 3. Environment access

From here on you operate autonomously, so collect access **now**, not
mid-experiment. Walk through what the plan needs and ask the user for each:

- hardware: which machines/testbed/GPUs, how to reach them (SSH host aliases,
  job scheduler), and what is off-limits;
- credentials/API keys, dataset locations and licenses;
- permission boundaries: what you may install, what you may run unattended,
  budget/quota limits (cloud spend, GPU hours);
- how long-running jobs should be handled (background, checkpoints).

Test each access path with a harmless read-only command before declaring it
working. Record the inventory (not the secrets themselves) in `paper/plan.md`.

Two lessons that cost real time when missed:

- **Machines created later count too.** If the plan will create new machines
  (VMs, containers, cloud instances), decide now how you will reach them —
  network path, jump host, DNS — and verify the pattern with one probe.
  A testbed you can build but not reach stalls the whole stage.
- **Probe gently.** Repeated SSH connection attempts trip fail2ban and edge
  rate limits, and getting banned mid-provisioning needs the user to rescue
  you. Back off between retries; never hammer a host in a loop.

## 4. Experiment plan

Write the evaluation *before* building — it is the contract the
implementation must satisfy. In `paper/plan.md`:

- **Research questions.** RQ1..RQn, each mapping to one contribution claim
  from the proposal. Typical shape: end-to-end gain, where the gain comes
  from (ablation), scaling behavior, overheads.
- **Baselines.** State of the art (authors' code where available, fairly
  tuned), a naive baseline, and variants of our own system for ablations.
- **Workloads/datasets.** Prefer standard suites; no cherry-picking subsets.
- **Metrics.** Justify each; means *and* tails (p99) for latency work;
  accuracy *and* cost for ML work.
- **Rigor budget.** Runs per configuration (≥5 for perf, ≥3 seeds for ML),
  error bars, and how variance will be reported.
- **Kill criteria.** For each RQ, what result would falsify the claim — and
  what happens then (per the orchestrator: claims shrink or work loops back).

## Gate G2

Present venue.md + plan.md + the access inventory, with your recommendation
already embedded. On approval, update STATE.md and proceed to implementation.
