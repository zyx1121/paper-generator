# HCI venue profile

> Facts verified: 2026-08-06 — format rules (pages, templates, checklists,
> deadlines-adjacent mechanics) decay yearly; re-verify against the live CFP
> before relying on them.

Venues: CHI, UIST, CSCW. Grounded in full reads of Augmented Physics
(UIST'24 Best Paper, artifact), Infrastructuring Care (CHI'23 Best Paper,
qualitative diary study), Crossing the Threshold (CSCW'23 Best Paper,
ethnography), and The Benefits of Prosociality towards AI Agents
(CHI'25 Best Paper, randomized online experiment, N=295,
[arXiv:2502.02911](https://arxiv.org/abs/2502.02911)), plus the live
CHI/UIST/CSCW author guides and the CHI reviewing guide. **Sample is
n=4, one paper per genre** — every per-genre claim below rests on a
single paper unless the text says otherwise.

## Format facts

The three venues run three different length regimes and three different
column formats. Do not template one across all three — at every one of
them the wrong template is grounds for desk rejection.

- **CHI** (2026 author guide) — word count, not pages. Short papers
  ≤5,000 words; standard papers 5,000–12,000, "about 7,000-8,000 words
  on average"; over 12,000 "will be desk-rejected if their length is not
  justified". The count excludes references, figure/table captions, and
  appendices. A **single-column** format "must be used for the reviewing
  phase", and "use of different templates or formats may result in desk
  rejection". Anonymization violations — including inside supplemental
  material or in linked datasets and code repos — are desk-rejected.
  Four or more reviewers including ACs, plus a revise-and-resubmit phase
  for papers above a threshold.
- **UIST** (2026 author guide) — "a page limit instead of a word limit.
  Therefore, we ONLY accept submissions in the 2-column format."
  10 pages standard, 5 pages short, **two-column**
  `\documentclass[sigconf,review,anonymous]{acmart}`. References and
  appendices are excluded from the count; acknowledgements are not.
  Over the limit = desk reject; up to +10% length after conditional
  accept. Review: at least four people (1AC, 2AC, two externals), and
  **only the 1AC knows the authors' identities**; about a week for a
  self-contained 5,000-character rebuttal; the 1AC verifies the revision
  before the conditional accept becomes an accept.
- **CSCW / PACM HCI** — rolling submission into a journal track, not one
  conference deadline. "If a paper is shorter than 5000 words or exceeds
  12,000 words, it will be subject to additional scrutiny." The
  **single-column** `acmsmall` PACM HCI template is required and "papers
  that use a completely different template will be desk rejected".
  Anonymization must strip "universities, companies, labs, and cities".
  Decisions are Conditional Accept with Minor Changes / Revise and
  Resubmit / Reject, with the same reviewers across rounds where
  possible, roughly 3–4 months to the first decision.
- Review axes (CHI guide): contribution significance, originality,
  research quality/rigor (defined per sub-community), presentation
  clarity, related-work coverage.

## Three genres — branch first

HCI is several genres sharing venues. Wobbrock & Kientz's seven
contribution types (empirical, artifact, methodological, theoretical,
dataset, survey, opinion) are the community's own vocabulary — name your
type early and match its skeleton:

- **Artifact** (UIST-style): Intro → Related Work → Formative study →
  System (walkthrough + separate Implementation subsection) → Evaluation
  (usability + expert interviews) → Discussion.
- **Qualitative** (CHI/CSCW-style): Intro → Background + Related Work →
  Method (with positionality) → Findings (themes) → Discussion →
  Conclusion. No formative study, no system section.
- **Quantitative / experimental** (CHI-style empirical study): Intro →
  Related Work *that terminates in numbered hypotheses and RQs* →
  Method (Materials → Procedure → Participants → Measurement → Analysis)
  → Results (manipulation check first, then one subsection per
  hypothesis/RQ) → Discussion (including Design Implications) →
  Limitations → Conclusion. The CCS concept is "Empirical studies in
  HCI"; there is no system section and no formative study.

## Title

Main title + colon + descriptive subtitle in all four papers, but the
*main* title is genre-bound. Artifact main titles are product names;
qualitative main titles are verbed concepts ("Infrastructuring Care",
"Crossing the Threshold"); the experimental paper is plainly descriptive
on both sides of the colon ("The Benefits of Prosociality towards AI
Agents: Examining the Effects of Helping AI Agents on Human Well-Being").
The metaphor/slogan main title is a qualitative-and-artifact move — do
not force one onto an experiment paper. Subtitles may be How-questions.

## Abstract

140–175 words across the four papers (well under CHI's cap).
Near-verbatim community idiom: "we present/discuss N themes/contributions".
Placement of the method/scale sentence splits by genre: artifact and
qualitative papers put it first or second ("a cross-cultural diary study
with 64 participants in…"), the experimental paper puts it *third*,
after a phenomenon sentence and a gap sentence ("To address this, we
conducted an experiment (N = 295) to explore…").

- Artifact moves: what the system is → tech → context of use → formative
  study source → evaluation methods with Ns → takeaway.
- Qualitative moves: method+N+population → analysis lens → finding
  constructs → contribution / call to action (a normative closing
  sentence is acceptable).
- Experimental moves: established effect among humans → unknown for the
  new context → design + N → one clause per outcome measure **including
  the nulls and the reversal** → "we discuss the implications of these
  findings for…".

## Introduction

- Artifact: narrative paragraphs unfolding each contribution, then a
  numbered contribution list restating them at the end (deliberate
  redundancy).
- Qualitative: RQ1/RQ2 stated in the intro plus full-sentence numbered
  contributions, or pure "Firstly/Secondly/Finally" narrative repeated
  verbatim in the Conclusion with completed-tense verbs.
- Experimental: an epigraph is tolerated; then motivation → two gap
  paragraphs (one per unknown) → a one-paragraph study summary naming
  the design, N, and every result → "Our research presents several
  contributions to HCI. Firstly… Secondly… Thirdly…". The RQs are *not*
  in the intro; they arrive at the end of Related Work.

## Related work — early, always

Immediately after the Introduction in all four papers (opposite of
systems/networking). Thematic subsections; qualitative papers spend far
more here (12–24% of the paper) than artifact or experimental papers
(~10–11%) and may split it into Background (social/political context) +
Related Work (concepts). Every review ends with an explicit gap
statement bridging to the next section.

In experimental papers the gap statement is *load-bearing*: each
subsection ends by converting its gap into a numbered, testable
hypothesis ("H1: Helping AI agents improves people's well-being,
including (a)… (d)…") or, where no directional prediction is warranted,
into RQ1/RQ2. Related work therefore doubles as hypothesis development,
and every hypothesis must be traceable to the literature that motivated
it.

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

## Statistics and quantitative rigor (experimental papers)

From the single experimental paper read end-to-end — a template to copy,
not a community census. Approximate shares of its body text: Method 31%,
Discussion+Conclusion 35%, Results 17%, Related Work 11%.

- **Method carries the paper.** Fixed subsections, in order: Materials
  (one per task and per manipulation, quoting the verbatim interface
  text and the exact wording of every prompt), Procedure (with a flow
  figure, plus a paragraph justifying the *ordering* of the steps),
  Participants, Measurement, Analysis.
- **A priori power analysis, in Participants, with every input stated**:
  "A power analysis (power = .80, significance level = .05, effect size
  f = .25, number of groups = 9) indicated that a minimum of 252
  participants was needed, with at least 28 participants in each group."
- **Exclusions with exact Ns and reasons** (93 who declined to help, 48
  attention-check failures → 295 analyzed), then recruitment platform,
  ethics-committee approval, compensation (USD $3), and session duration
  with a citation justifying it.
- **Validated scales cited by name** (PANAS, Rosenberg self-esteem,
  Hughes 3-item loneliness), a stated Likert range, one sample item per
  scale, and Cronbach's α reported *per measurement point* (baseline and
  post). Manipulation-check items get the same treatment.
- **The Analysis subsection justifies the test choice before any test
  runs**: Levene for homogeneity of variance and Shapiro–Wilk for
  normality; normality failed, so non-parametric throughout
  (Mann–Whitney U, Kruskal–Wallis with post-hoc Dunn and Bonferroni
  correction), with a log transform plus t-test/ANCOVA used only where
  control variables were required. Never present a test without this
  chain, and state which covariates were controlled and why.
- **Inline reporting format**: M and SD for *both* sides of every
  comparison, then the statistic and p — `(M = -0.47, SD = 0.88 …
  W = 5451, p < 0.05)`, `H(2) = 16.84, p < 0.001`,
  `F(2, 291) = 4.50, p < 0.05`. Significant results are thresholded
  (p < 0.05 / 0.01 / 0.001); non-significant ones carry the exact p
  (p = 0.10), and marginal ones are named as such.
- **No standardized effect sizes anywhere in the results** — no d, no η²,
  no r; effect size appears only as the power-analysis input. A CHI Best
  Paper did exactly this, so omitting them is survivable, but reviewers
  from psych-adjacent sub-communities do ask. Report them, or be ready
  to defend the omission.
- **Results subsections are claim sentences tagged with their
  hypothesis**: "Helping AI Reduces People's Loneliness (H1)". The
  manipulation check is the *first* Results subsection, ahead of any
  hypothesis test.
- **Nulls and reversals are stated plainly, not buried** ("These results
  supported hypothesis H1(d) but did not support H1(a), H1(b), or
  H1(c)"), and a closing table maps every hypothesis and RQ to
  Supported / Not Supported.
- **Display items — this genre is not figure-light**: 6 figures and
  3 tables in an 18-page paper. A page-1 conceptual figure summarising
  the study focus; screenshots of each manipulation condition; an
  experiment-flow figure; box plots (whiskers min–max, box 25th–75th,
  median line, mean dot) with the significance-star key defined in the
  caption; an interaction plot. Tables: per-group demographics, per-group
  M/SD with Bonferroni-corrected p, and the hypothesis/RQ summary.

## Implications — the post-Dourish turn is qualitative-only

The avoidance of "Implications for Design" is a *qualitative* norm, not a
venue-wide one — do not over-apply it.

- **Qualitative**: recent award-level papers avoid the heading. They
  close with a research agenda or embed conditionals in Findings ("If
  makerspaces could audit…, women may feel more welcome"), sometimes
  explicitly declining to list design recommendations. Do not bolt a
  generic implications list onto qualitative work.
- **Artifact**: delivers design implications directly — they *are* the
  design strategies.
- **Experimental**: the CHI'25 Best Paper carries a full "Design
  Implications" subsection of the Discussion, reasoning from each
  manipulation to a concrete design move, and pairing each move with its
  ethical limit ("creating fake scenarios where AI agents appear to need
  help, but actually do not, may undermine people's trust"). It also
  flags which recommended techniques were *not* validated by the study.
  Do not strip this section out of experimental work.

Across genres the Discussion is the largest section, and in the
experimental paper it is larger than Results (35% vs 17%): interpretation,
not the test statistics, is what carries an HCI paper. Limitations is its
own Discussion subsection with an enumerated "Firstly/Secondly/…/Finally"
list, each item pairing a scope limit with the study that would fix it.

## Positionality and tone

Qualitative work involving marginalized populations carries a positionality
statement (its own Methods subsection, or woven in via "the first
author…"). The convention holds in both qualitative papers read (n=2) and
is *absent* from both the artifact and the experimental paper, so it reads
as genre-bound rather than venue-wide — but two positive cases is a thin
base, so check a recent paper in your own sub-community before deciding.
"We" throughout; system description in present tense, studies in past.

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
  design, walkthrough clarity; experimental — power analysis with stated
  inputs, exclusion accounting, manipulation checks reported before
  results, scale reliability, assumption tests preceding the choice of
  statistical test, multiple-comparison correction, and whether nulls are
  reported as plainly as the significant effects.
- **C — significance reader**: "why should the CHI community care";
  does the length match the contribution size (venue rule).
- **Field must-checks**: do **not** demand statistics or generalizability
  from qualitative work; do **not** demand a generic "Implications for
  Design" list from post-Dourish qualitative papers — a research agenda or
  embedded conditionals is the current award-level norm, but experimental
  and artifact papers *should* carry one. Do **not** apply CHI's word
  limits to a UIST submission (pages, two-column) or a CSCW submission
  (rolling, `acmsmall`); the length regimes are genuinely different.
