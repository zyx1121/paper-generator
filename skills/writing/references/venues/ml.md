# Machine learning venue profile

> Facts verified: 2026-08-06 — format rules (pages, templates, checklists,
> deadlines-adjacent mechanics) decay yearly; re-verify against the live CFP
> before relying on them.

Venues: NeurIPS, ICML, ICLR. Grounded in full reads of LoRA (ICLR'22),
DPO (NeurIPS'23), Chinchilla (NeurIPS'22), Emergent-Abilities-Mirage
(NeurIPS'23 Outstanding), plus the live checklist/CFP pages.

## Format facts

- **Single column** — the visual tell against every other CS community.
- Body pages: NeurIPS 9, ICML 8, ICLR 10; references and appendix
  unlimited, reviewers not obliged to read the appendix — the body must be
  self-contained.
- NeurIPS: submission without the completed paper checklist (16 items,
  including the LLM-usage declaration) is desk-rejected. ICML impact
  statement and ICLR ethics/reproducibility statements are softer
  (optional or reputation-only).
- Anonymity desk-reject at ICLR: citing your own arXiv version in first
  person; placeholder abstracts.

## Title

Sober-descriptive dominates: "Name: description" (LoRA) or plain
description (Chinchilla). Question titles exist for debunking/empirical
papers ("Are Emergent Abilities of LLMs a Mirage?"). Wordplay goes in the
subtitle, not the main title (DPO: "Your Language Model is Secretly a
Reward Model"). "X is all you need" is a real meme and a known reviewer
irritant — don't.

## Abstract

180–200 words, 5–9 sentences. Moves: problem → gap → method → quantified
result → claim/release statement. Both number styles are legitimate:
LoRA packs multipliers (10,000×, 3×), DPO carries no numbers and defers
them to the body. Pick one; don't split the difference.

## Introduction

Moves: big-picture motivation → existing approaches fall short (can carry a
run-in like "Aren't existing solutions good enough?") → insight/hypothesis
→ contribution statement citing Figure 1 → advantages. Contribution form
varies: bolded-lead bullets (LoRA), a narrative sentence (DPO), or numbered
methods (Mirage) — bullets are not mandatory here. **Figure 1 is a teaser**:
mechanism diagram, pipeline contrast, or the phenomenon under attack.
A one-line roadmap is tolerated at ML venues.

## Related work

Genuinely unfixed: §2 when the reader needs the lineage before the method
(DPO), §6 near the end when it is positioning only (LoRA, Mirage). Choose
by dependency, then keep it.

## Method

Notation defined inline at first use (W₀ ∈ ℝ^(d×k)) before update rules.
Theorem apparatus only if the paper is actually theoretical: DPO uses
Definition/Lemma/Theorem with proof sketches in the body and full proofs in
Appendix A; LoRA and both empirical papers use numbered equations only.
(Algorithm blocks: no example in the four papers read — *uncertain*, check
an RL/optimizer paper before templating.)

## Experiments

- Subsection naming, two live modes: dataset/model-driven ("RoBERTa
  base/large") or question-driven ("How well can DPO optimize the RLHF
  objective?").
- Main table: bold-best + ±std over ≥3 seeds is the default but not
  universal — Chinchilla uses bootstrap percentile intervals, DPO win rates.
  Whichever, the uncertainty convention must be stated.
- Setup: one or two sentences in the body; full hyperparameter tables,
  hardware, dataset details in the appendix.
- Ablation: every novel component; "Prediction: X" subsection framing works
  for hypothesis-driven empirical papers.

## Appendix culture

Heavy and expected: full proofs, full hyperparameters, extra ablations,
dataset documentation. Anything a reviewer might demand but not read goes
there; anything the claims depend on stays in the body.

## Tone

"We" + present tense (we find / observe / show / hypothesize); past tense
for what was run. Hedging: "suggests that", "may", "to our surprise".
After naming the method once, refer to it only by its acronym — never
"our method". Debunking papers may take a combative register ("we call
into question…"); method papers should not.

## Reviewer expectations

Checklist completeness (NeurIPS: hard gate), stated limitations (reviewers
are instructed to reward them), reproducibility (code/seeds/splits),
statistical significance, compute disclosure. Over-page enforcement
mechanics are venue-year-specific (*uncertain* — check the current CFP).

## Reviewer personas at this venue

- **A — domain expert (recent-arXiv sweep)**: the field moves in months,
  not years — hunt missing baselines and concurrent work from the last
  12 months, and whether the headline gain holds against the *strongest*
  recent baseline, not a convenient older one.
- **B — reproducibility/checklist auditor**: seeds, splits, compute budget,
  hyperparameter disclosure, statistical significance across seeds; is the
  body self-contained without the appendix; does every checklist "yes"
  point at a section that actually delivers it.
- **C — busy area-chair-adjacent reader**: does the teaser Figure 1
  oversell; are limitations stated (reward them — venue policy); is the
  method reproducible from the paper alone.
- **Field must-checks**: checklist present and honest (missing = desk
  reject at NeurIPS); ablation for every novel component; no bare "SOTA"
  claims without the comparison table. Do **not** penalize related work
  at §6 or a one-line roadmap — both are legitimate here.
