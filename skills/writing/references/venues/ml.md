# Machine learning venue profile

> Facts verified: 2026-08-06 — format rules (pages, templates, checklists,
> deadlines-adjacent mechanics) decay yearly; re-verify against the live CFP
> before relying on them.

Venues: NeurIPS, ICML, ICLR. Grounded in full reads of LoRA (ICLR'22),
DPO (NeurIPS'23), Chinchilla (NeurIPS'22), Emergent-Abilities-Mirage
(NeurIPS'23 Outstanding), plus algorithm-block reads of PPO
(arXiv 1707.06347), AdamW (arXiv 1711.05101) and VAR (arXiv 2404.02905,
NeurIPS'24 Best Paper), and the 2026-edition CFPs / author guides /
checklist guide.

## Format facts

- **Single column** — the visual tell against every other CS community.
- Body pages, 2026 editions: **NeurIPS 9** content pages; **ICML 8** at
  submission (9 for the camera-ready, one extra page granted); **ICLR 9**
  at submission, raised to 10 for the rebuttal phase and camera-ready.
  References, appendices, ICML's impact statement and NeurIPS's checklist
  are all free. Reviewers are not obliged to read the appendix — the body
  must be self-contained.
- Over-page enforcement is real at all three; only the verb differs.
  ICML 2026 author instructions: "any submission whose main body goes over
  the 8 page limit will be automatically rejected". ICLR 2026 author
  guide: "This limit will be strictly enforced. Papers with main text
  beyond the page limit will be desk-rejected." NeurIPS 2026 handbook is
  the only discretionary one: submissions that violate the style "or page
  limits **may** be desk rejected". Treat all three as hard — there is no
  half-page grace anywhere.
- NeurIPS: the paper checklist (16 items, last one the declaration of LLM
  usage) is mandatory — "authors are required to complete the paper
  checklist included in the paper template". No current NeurIPS text says
  a *missing* checklist is auto-desk-rejected; the operative clause is the
  generic "papers may also be rejected without consideration of their
  merits if they fail to meet the submission requirements". ICML's impact
  statement is required but satisfiable with the CFP's own boilerplate;
  ICLR's ethics and reproducibility statements are optional and merely
  recommended, and neither counts toward the page limit.
- Anonymity desk-reject at ICLR: citing your own arXiv version in first
  person; placeholder abstracts. ICLR also desk-rejects non-disclosure of
  LLM use that "significantly contributed to research ideation and/or
  writing" — a separate section is required in that case.

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

**Algorithm blocks.** Reach for `\begin{algorithm}` only when the
contribution carries control flow the equations cannot: loop nesting,
what is collected before what is updated, how many passes over which
minibatch. PPO is the clean case — §5 states the objective as numbered
equations (9)–(12), then ends with "Algorithm 1 PPO, Actor-Critic Style"
whose entire body is the loop skeleton ("for iteration=1,2,… do / for
actor=1,2,…,N do / Run policy π_θold in environment for T timesteps /
Compute advantage estimates … / end for / Optimize surrogate L wrt θ, with
K epochs and minibatch size M ≤ NT / θold ← θ / end for"). It restates no
formula: equations say *what* is optimized, the box says *in what order*.
Duplicating the loss inside the box is the common novice move — don't.
Placement is the body, not the appendix, and specifically inside or at the
end of the method section: PPO's box closes §5 immediately before the
Experiments section; VAR puts Algorithm 1 (multi-scale VQVAE encoding) and
Algorithm 2 (reconstruction) in §3.2, mid-method. Captions split two ways
— title-only naming the method ("PPO, Actor-Critic Style") or a full
descriptive sentence when one box compares two variants (AdamW's
Algorithm 2: "Adam with L2 regularization and Adam with decoupled weight
decay (AdamW)"). AdamW additionally colour-highlights the single line that
differs from the baseline algorithm; copy that idiom when the contribution
*is* one changed update rule. If the method is a loss or a scaling law
with no ordering to convey, skip the box — LoRA, DPO, Chinchilla and
Mirage all ship none.

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

## NeurIPS checklist, as it actually appears

Not a web form — a typeset section of the PDF, placed after the references
*and* after the appendices, last thing in the file, costing no page budget.
Layout per item: a numbered subsection title ("1. Claims", "2.
Limitations", …), then `Question:` reproduced verbatim from the template,
then `Answer: [Yes]` / `[No]` / `[NA]`, then `Justification:` in one or two
sentences, then the template's `Guidelines:` bullet block, which authors
keep rather than delete. Justifications name the section that delivers the
claim — a real filled example reads "Justification: Section 7 discusses
limitations, including challenges in handling non-convex solution mappings
and potential directions for improving efficiency…" (arXiv 2505.04037).
Per the official guide, "[No]" or "[NA]" with a proper justification "is
not grounds for rejection"; the actual failure mode is a "[Yes]" pointing
at a section that does not deliver it.

## Tone

"We" + present tense (we find / observe / show / hypothesize); past tense
for what was run. Hedging: "suggests that", "may", "to our surprise".
After naming the method once, refer to it only by its acronym — never
"our method". Debunking papers may take a combative register ("we call
into question…"); method papers should not.

## Reviewer expectations

Checklist completeness (NeurIPS: mandatory, and reviewers are told to use
it while reviewing), stated limitations (reviewers are instructed to reward
them), reproducibility (code/seeds/splits), statistical significance,
compute disclosure. Over-page enforcement is not a judgement call: ICML
auto-rejects over 8 pages, ICLR desk-rejects over its limit "strictly",
NeurIPS reserves discretion — see Format facts, and re-check the current
CFP each cycle since the numbers move.

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
- **Field must-checks**: checklist present and honest (mandatory at
  NeurIPS; an unjustified "[Yes]" is the real failure, not a justified
  "[No]"); ablation for every novel component; no bare "SOTA"
  claims without the comparison table. Do **not** penalize related work
  at §6 or a one-line roadmap — both are legitimate here.
