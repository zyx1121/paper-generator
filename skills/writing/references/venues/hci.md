# HCI venue profile

> Facts verified: 2026-08-06 — format rules (pages, templates, checklists,
> deadlines-adjacent mechanics) decay yearly; re-verify against the live CFP
> before relying on them.

Venues: CHI, UIST, CSCW. Grounded in full reads of Augmented Physics
(UIST'24 Best Paper, artifact), Infrastructuring Care (CHI'23 Best Paper,
qualitative diary study), Crossing the Threshold (CSCW'23 Best Paper,
ethnography), plus the CHI reviewing guide.

## Format facts

- Word-count regime, not page-count: CHI 5,000–12,000 words excluding
  references/captions/appendix; length must be justified by contribution
  size or desk reject. Single-column ACM master template.
- Review axes (CHI guide): contribution significance, originality,
  research quality/rigor (defined per sub-community), presentation
  clarity, related-work coverage.

## Artifact vs. qualitative — branch first

HCI is two genres sharing venues. Wobbrock & Kientz's seven contribution
types (empirical, artifact, methodological, theoretical, dataset, survey,
opinion) are the community's own vocabulary — name your type early and
match its skeleton:

- **Artifact** (UIST-style): Intro → Related Work → Formative study →
  System (walkthrough + separate Implementation subsection) → Evaluation
  (usability + expert interviews) → Discussion.
- **Qualitative** (CHI/CSCW-style): Intro → Background + Related Work →
  Method (with positionality) → Findings (themes) → Discussion →
  Conclusion. No formative study, no system section.

## Title

Metaphor/slogan main title + colon + descriptive subtitle, in all three
papers. Artifact main titles are product names; qualitative main titles
are verbed concepts ("Infrastructuring Care", "Crossing the Threshold").
Subtitles may be How-questions.

## Abstract

140–165 words (well under CHI's cap). The method/scale sentence comes
first or second ("a cross-cultural diary study with 64 participants in…").
Near-verbatim community idiom: "we present/discuss N themes/contributions".
Artifact moves: what the system is → tech → context of use → formative
study source → evaluation methods with Ns → takeaway. Qualitative moves:
method+N+population → analysis lens → finding constructs → contribution /
call to action (a normative closing sentence is acceptable).

## Introduction

- Artifact: narrative paragraphs unfolding each contribution, then a
  numbered contribution list restating them at the end (deliberate
  redundancy).
- Qualitative: RQ1/RQ2 stated in the intro plus full-sentence numbered
  contributions, or pure "Firstly/Secondly/Finally" narrative repeated
  verbatim in the Conclusion with completed-tense verbs.

## Related work — early, always

Immediately after the Introduction in all three papers (opposite of
systems/networking). Thematic subsections; qualitative papers spend far
more here (12–24% of the paper vs ~10% for artifact) and may split it into
Background (social/political context) + Related Work (concepts). Every
review ends with an explicit gap statement bridging to the next section.

## Formative study → system (artifact only)

N≈7 experts, two-phase (open discussion → design elicitation). The
conversion sentence is a template: "From their feedback, we identified N
primary categories/strategies." System walkthrough as numbered operation
steps ("1) Import… 2) Choose… 3) Extract…"); engineering stack isolated in
an Implementation subsection.

## Studies and qualitative rigor

- Report N, recruitment path, compensation amounts, analysis method by
  name (Reflexive Thematic Analysis, grounded theory), number of coders
  and how disagreement was resolved.
- Quote attribution convention: identifier + population attributes
  ("P25, a Black non-binary person in the Northeastern U.S.").
- Themes get narrative subsection titles, never "Theme 1/2/3".

## Implications — the post-Dourish turn

Only artifact papers still deliver design implications directly (they are
the design strategies). Recent award-level qualitative papers *avoid* the
"Implications for Design" heading: they close with a research agenda or
embed conditionals in Findings ("If makerspaces could audit…, women may
feel more welcome"), sometimes explicitly declining to list design
recommendations. Do not bolt a generic implications list onto qualitative
work.

## Positionality and tone

Qualitative work involving marginalized populations carries a positionality
statement (its own Methods subsection, or woven in via "the first
author…"); artifact papers have none. "We" throughout; system description
in present tense, studies in past.

## Reviewer personas at this venue

Before anything else, **classify the contribution type** (Wobbrock's
seven) — rigor at CHI is judged *relative to the contribution type*, so a
reviewer applying artifact standards to qualitative work (or vice versa)
is miscalibrated by construction.

- **A — domain expert**: related-work coverage (it sits early here and is
  scrutinized); whether the framing engages the sub-community's own
  concepts and debates, not just adjacent CS.
- **B — methods reviewer, type-matched**: qualitative — recruitment path,
  compensation, analysis method named, coder count and disagreement
  handling, quote attribution, positionality where the population warrants
  it; artifact — formative-study grounding, usability + expert evaluation
  design, walkthrough clarity.
- **C — significance reader**: "why should the CHI community care";
  does the length match the contribution size (venue rule).
- **Field must-checks**: do **not** demand statistics or generalizability
  from qualitative work; do **not** demand a generic "Implications for
  Design" list from post-Dourish qualitative papers — a research agenda or
  embedded conditionals is the current award-level norm.
