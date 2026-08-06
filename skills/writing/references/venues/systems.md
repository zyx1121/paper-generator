# Systems / cloud infrastructure venue profile

> Facts verified: 2026-08-06 — format rules (pages, templates, checklists,
> deadlines-adjacent mechanics) decay yearly; re-verify against the live CFP
> before relying on them.

Venues: OSDI, SOSP, ATC, EuroSys (USENIX/ACM tier); ICDCS, IC2E, Middleware
(IEEE/ACM second tier). Grounded in full reads of ServerlessLLM (OSDI'24),
vLLM (SOSP'23), Tangram (ICDCS'24), plus a title census of six 2024
programs (~90 titles) and the ICDCS/Middleware CFPs.

## Format facts

- USENIX tier: 2-column, 12 pp body, references/appendix free. OSDI/SOSP
  explicitly down-rank padded papers — "the right length may be less than
  12 pages" (*uncertain: secondhand CFP quote*).
- ICDCS: IEEE 2-column 10pt, **11 pp including references**; over-length or
  shrunken fonts = desk reject. Middleware: ACM sigconf **9pt**, 12 pp
  technical content, revision-cycle decisions. Double-blind throughout.

## The two tiers write differently

Three confirmed differences (IEEE-tier evidence is n=1 close read + title
census — treat as defaults, not laws):

1. IEEE tier inserts a dedicated **Motivation/Challenge section** before
   Design; USENIX tier folds motivation into §1–2.
2. IEEE tier states contributions in **narrative prose** and includes an
   explicit roadmap paragraph; USENIX tier uses contribution bullets and
   omits the roadmap.
3. Numbers: USENIX tier headlines **rounded multipliers** (2–4×, 10–200×);
   IEEE tier quotes **two-decimal percentages** (74.30%).

## Title

`SystemName: Claim` is the default (EuroSys'24: 14/14; OSDI'24: 10/15).
Inverted variant: claim first, "with SystemName". Do not hard-code the
colon: vLLM's title has no colon and no system name — the algorithm name
carries it. IC2E tolerates question titles; OSDI/SOSP/EuroSys don't use them.

## Abstract

4–8 sentences, 120–160 words. Two openings, both legitimate:
problem-first (context → problem → solution → result) or system-first
("This paper presents X, a … that …"). One or two headline numbers, rounded
(USENIX) or precise (IEEE). Optional last sentence: artifact link.
Do not thread more than ~3 numbers through the abstract — density of inline
percentages reads as foreign at these venues.

## Introduction

6–7 paragraphs: domain stakes → technical bottleneck → problem quantified
(cite Figure 1) → key observation ("We observe that …") → system + headline
number → contribution bullets (USENIX: 3–4 bullets, "We identify / We
propose / We design and implement / We evaluate", each with a §-ref;
IEEE: prose + roadmap paragraph). Figure 1 is an overview or motivating
measurement; its caption is a descriptive label, not a claim sentence.

## Design

- Open by pointing back at the problem section in one sentence, then either
  an architecture figure walk (vLLM) or a named list of design concerns that
  map 1:1 onto the following sections (ServerlessLLM).
- IEEE-tier papers may add a formal problem/optimization statement —
  accepted there, out of place at USENIX tier.
- Present tense; subject is the system name or "we". State design claims
  flatly; reserve hedging for empirical observations.

## Evaluation — NOT organized by RQs

No top systems paper read uses RQ1/RQ2 headers (that is SE dialect). The
canonical shape:

1. **Experimental Setup** (always first): testbed, versions, workloads,
   named baselines and tuning, metrics, runs/variance.
2. **Per-component / per-workload subsections** — named after the component
   ("X Checkpoint Loading", "X Model Scheduler") or the workload ("Chatbot",
   "Shared prefix").
3. **End-to-end / integration** — community idiom for the title: "Entire X
   in Action", "Deep Dive into X".
4. **Ablation** — its own subsection or top-level section.
   IEEE tier may add a dedicated **Accuracy** subsection.

Baselines are named systems (never just "baseline"); include an oracle
upper bound where one exists. Narrate claim-first: state "X sustains
1.7–2.7× higher rates than Orca" before walking the figure. Line charts for
latency-vs-load, bars for memory/cost, CDFs in deep-dive subsections.

## Related work

Late — after Evaluation, before Conclusion. USENIX tier: flat thematic
paragraphs with topic sentences; IEEE tier: named subsections. Highest
citation density of any section (24–29 refs typical; papers carry 60–90
total). Every cluster ends with a differentiator: "However/Unlike [prior],
[System] …". Name the single closest system and state the relationship
explicitly (complementary vs. superseding).

## Figures, tables, citations

12–19 figures, 0–1 tables at USENIX tier (specs can live in prose); IEEE
tier uses a results table. Captions are descriptive labels — the
"caption states the finding" advice is not how these venues write
(*confirmed across all three papers read*).

## Reviewer expectations

Middleware's published criteria: significance, novelty, advancement beyond
prior work, sufficient supporting evidence, clarity. Classic kills: missing
closest-system baseline, evaluation that dodges the paper's own claims,
padding. Desk rejects: page/format violations (ICDCS explicit), broken
anonymization.

## Reviewer personas at this venue

- **A — domain expert**: lives in the serving/serverless/checkpoint
  literature. Hunts the uncited closest *system* (the classic systems kill:
  "you didn't compare against X"), overlap with named prior systems, and
  whether the stated delta survives a read of those systems' papers.
- **B — methods hawk (SIGPLAN empirical)**: baselines fairly tuned, run
  counts and variance, tails not just means, workload cherry-picking,
  ablations attributing the gain — and padding: down-rank filler, per OSDI
  culture ("the right length may be less than 12 pages").
- **C — busy PC member**: 15 papers in the stack. Does the contribution
  list survive the details; is Figure 1 comprehensible alone; does the
  design section give rationale for each contestable choice.
- **Field must-checks**: evaluation shaped setup → components → end-to-end
  → ablation (RQ headers read as SE dialect — flag); related work late with
  explicit differentiators; claim-first narration backed by the cited
  figure. Do **not** demand a Threats-to-Validity section or RQ headers —
  wrong field.
