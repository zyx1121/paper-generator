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

Also record the matching **venue profile** in `paper/venue.md` (e.g.
`profile: skills/writing/references/venues/systems.md`) — pick from the
index at `skills/writing/references/venues/README.md`. The profile drives
field-specific structure (evaluation organization, related-work placement,
signature sections, tone) in the writing and review stages. If no profile
fits, write `profile: none` and note why.

Record the venue's **artifact regime** in `venue.md` at the same time:
separate artifact evaluation with badges (typical for systems, security,
SE — note the AE deadline relative to notification), checklist-tied code
release (ML), or none. Stage 8 prepares the package; knowing the regime
now is what keeps `experiments/` provenance AE-ready instead of
retrofitted.

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
  Every baseline gets a name — "baseline" is not one — plus an oracle upper
  bound wherever one exists.
- **Workloads/datasets.** Prefer standard suites; no cherry-picking subsets.
  Fix the workload list before the first result, not after.
- **Metrics.** Justify each; means *and* tails (p99) for latency work;
  accuracy *and* cost for ML work.
- **Rigor budget.** Field-specific — see §4.1.
- **Kill criteria.** For each RQ, what result would falsify the claim — and
  what happens then (per the orchestrator: claims shrink or work loops
  back). The *honest exit* is also field-specific: systems and networking
  shrink the claim to the regime that actually held (and say which regime);
  ML reports the negative result with an analysis of why — these venues
  instruct reviewers to reward stated limitations; SE keeps the RQ and
  discloses the failure in Threats to Validity; security folds the failed
  path back into the threat model as a scope limit (*uncertain*: inferred
  from limitations-section candor, not a stated venue rule); HCI reframes
  against the declared contribution type. Never silently drop an RQ that
  was in the approved plan.

### 4.1 Rigor budget by field

Read the profile recorded in `paper/venue.md` first, then apply the row
below; where the profile disagrees, **the profile wins**. Rigor currency is
not universal — the run count that satisfies a systems reviewer is not what
an ML reproducibility auditor asks for. `profile: none` → use the systems
row as the floor. Each row: currency, how variance is shown, what must be
recorded from day 1, what `plan.md` carries beyond the generic bullets.

- **Systems** — Currency: ≥5 runs per configuration; named baselines;
  tails (p95/p99) reported next to means. Variance: error bars on every
  aggregate, CDFs in deep-dive subsections. Day 1: exact testbed versions
  (hardware, OS/kernel, library and baseline commit hashes) and how each
  baseline was tuned. plan.md also carries: the evaluation shape — setup →
  per-component → end-to-end → ablation — with each planned figure
  assigned to one of those.
- **Networking** — Currency: the run count is a specific integer that will
  be printed in the paper ("100 experiments", "5 traces of 30–60 s");
  "several runs" is a rejection risk. Variance: CDFs with the median called
  out in prose, shaded std-dev regions, 2-D std ellipses. Day 1: exact
  hardware model numbers (chips, boards, FPGA, frequency, bandwidth, array
  size, ground-truth rig; commercial devices by model name) — missing
  system details the authors clearly had is the classic rejection. plan.md
  also carries: the oracle upper bound, and how each root cause will be
  *traced* (packet captures, raw traces) rather than asserted.
- **ML** — Currency: ≥3 seeds per reported cell; an ablation for every
  novel component; comparison against the strongest recent baseline, not a
  convenient older one. Variance: ±std over seeds *or* bootstrap CIs — pick
  one, state it, keep it across the paper. Day 1: seeds, data splits,
  hyperparameters, and compute budget (GPU-hours + hardware) logged as they
  are used; reconstructing them later is how checklists become dishonest.
  plan.md also carries: the venue checklist (NeurIPS: 16 items incl. the
  LLM-usage declaration; missing = desk reject) with each item mapped to the
  experiment or section that will answer it.
- **Security** — Currency: success rate as % + denominator + named baseline
  ("95.6% (44 of 46), whereas AURORA achieves 63.0%"), plus a per-case
  failure analysis naming which cases failed and why. Variance: denominators
  and case tables carry the weight; internet-scale measurements get their
  own methodology (scan scope, opt-out handling). Day 1: attack scope, IRB /
  human-subjects status. plan.md also carries: **the disclosure plan, fixed
  before the experiments run** — if this work may find a new vulnerability,
  write down vendors, notification timeline, CVE handling, and embargo
  (USENIX expects disclosure at discovery time; undisclosed vulnerabilities
  without justification are grounds for rejection; S&P: 45–90 days before
  publication). Deciding this after the finding is already too late.
- **SE** — Currency: 4–6 RQs, each with a rationale sentence and a
  visually marked answer; per-RQ statistics named up front (splits, folds,
  the statistical model). Variance: the named test plus effect size per RQ.
  Day 1: build the **replication package alongside the code**, not after —
  Verifiability and Transparency is one of ICSE's five review axes; log
  reproduction deltas against the original papers as you hit them ("within
  2% except X, because Y"). plan.md also carries: the replication-package
  plan (what ships, where, how it runs) and the manual-judgment protocol
  (coder count, disagreement resolution, owned bias).
- **HCI** — Currency: rigor is judged *relative to the declared
  contribution type* (Wobbrock's seven) — artifact: formative study plus
  usability + expert evaluation with Ns (N≈12 each is the read norm);
  qualitative: recruitment path, compensation, named analysis method,
  coder count. Variance: N= everywhere; statistics are not the currency for
  qualitative work and should not be manufactured. Day 1: recruitment plan,
  compensation amounts, consent/IRB, and positionality if the population
  warrants it. plan.md also carries: the contribution type, declared
  explicitly, and the study protocol per study.
- **Journals** — Currency: Transactions — completeness (full proofs, all
  cases covered, unfolded rather than padded); Nature/Science —
  reproducibility from a Methods section that sits at the very end, plus
  Data/Code availability. Day 1: the data/code availability target and, for
  a conference extension, a running list of what is new. plan.md also
  carries: the explicit delta over the conference version
  ("(a)… (b)… (c)…") — there is no official percentage rule, so the delta
  is judged on substance. (*uncertain*: grounded in ToN + Nature;
  TPDS/TSE/TOCS unverified.)

## Gate G2

Present venue.md + plan.md + the access inventory, with your recommendation
already embedded. On approval, update STATE.md and proceed to implementation.
