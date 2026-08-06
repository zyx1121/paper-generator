# Software engineering venue profile

> Facts verified: 2026-08-06 — format rules (pages, templates, checklists,
> deadlines-adjacent mechanics) decay yearly; re-verify against the live CFP
> before relying on them.

Venues: ICSE, FSE, ASE. Grounded in full reads of EDEFuzz (ICSE'24
Distinguished, tool), TypeGen (ASE'23 Distinguished, tool), *Pinning Is
Futile* (FSE'25 Distinguished, empirical/mining), and Steenhoek et al.'s
ICSE'23 empirical study on DL vulnerability detection — a regular
technical-track paper, **not** an award paper (it does not appear on ICSE
2023's Distinguished Paper list); it is here as a clean specimen of the
empirical-study shape, not as an exemplar of award writing. Section-level
reads of Threats to Validity and RQ handling add three ICSE'26 Distinguished
papers: *Evaluating Generated Commit Messages with LLMs* (empirical),
*The Hidden Cost of Readability* (empirical), *HoarePrompt* (technique).
This is the home of RQ-driven writing.

## Format facts

The three venues do **not** share a page shape. Check the venue, not the
field.

- **ICSE** (2026 research track): 2-column
  `\documentclass[sigconf,review,anonymous]{acmart}`; 10 pp main text
  inclusive of all figures, tables, and appendices, plus 2 pp of references
  only; accepted papers get one extra main-text page.
- **FSE** (2026 research papers): **single-column**
  `\documentclass[acmsmall,screen,review,anonymous]{acmart}`; 18 pp text and
  figures plus 4 pp references (20 + 4 for major revisions). Papers appear in
  *Proc. ACM on Software Engineering* (PACMSE), a journal issue, not
  conference proceedings. Non-compliant submissions are desk-rejected. Do not
  carry the ICSE 2-column shape to FSE.
- **ASE** (2026): 2-column `sigconf` acmart; 10 pp excluding references plus
  2 pp references; a **Data Availability Statement is mandatory**, placed
  after the Conclusions and inside the 10-page limit.

Review axes, verbatim from the venues' own CFPs:

- **ICSE 2026**: Novelty, Rigor, Relevance, Verifiability and Transparency,
  Presentation. The older list — Soundness, Significance, Novelty,
  Verifiability and Transparency, Presentation, where *Soundness* was defined
  as whether contributions "address its research questions" — is ICSE 2023
  and earlier; it was gone by ICSE 2025. **RQ-driven writing is a community
  habit, no longer anchored in the ICSE criteria.** Write RQs because the
  reviewers expect the genre, not because the CFP demands them.
- **FSE 2026**: "originality, importance of contribution, soundness,
  evaluation (if relevant), quality of presentation, and appropriate
  comparison to related work" — note the explicit related-work axis, which
  ICSE folds into Novelty.
- Verifiability in practice means an open replication package. ICSE has at
  least one reviewer check any attached or linked artifact; ASE requires the
  Data Availability Statement. Every paper read for this profile ships a
  package.

## RQ placement

Three placements are all in current use; pick by paper type, then commit.

- **Introduction, woven into motivating prose** — the RQ appears as a
  set-off bullet or bold line in the middle of the motivation, with the
  narrative resuming right after ("To answer this research question, we…").
  Used by the ICSE'23 empirical study, FSE'25 *Pinning*, and the ICSE'26
  commit-message study.
- **Top of a study-design section**, as a bare bullet list (ICSE'26 *Hidden
  Cost*, §2 Experimental Setting).
- **Top of Evaluation** — the tool/technique default (EDEFuzz, TypeGen,
  HoarePrompt).

For the body, **RQ-as-section-title is the dominant organization and is not
tool-only**: `3 RQ1: <the full question>` with `Method` / `Results`
subsections is exactly what both the FSE'25 and the ICSE'26 empirical papers
do. The thematic "Research Questions and Findings" grouping with
**Motivation → Study Setup → Findings** run-ins (ICSE'23 study) is one valid
option, not the norm (*n=1*).

## RQ craft

- **Count: 2–6.** Two in *Pinning*, three in the commit-message and *Hidden
  Cost* studies, four in HoarePrompt, six in the ICSE'23 study. Do not pad to
  hit a number; a two-RQ paper won a Distinguished award.
- Verb moods: Do/Are/How does judgment questions (empirical), How effective /
  What is the impact (tool). An RQ may embed its own metric definition.
- **Rationale sentence: usual, not universal — and it precedes the question
  at least as often as it follows.** "Thus, we ask RQ1: …" after a paragraph
  of motivation (commit-message study, *Pinning*) is as common as the
  trailing "This helps us understand…". Bare bullet RQs with no rationale at
  all appear in award-winning papers (HoarePrompt §5, *Hidden Cost* §2).
  Default to giving each RQ a rationale clause; do not read a bare list as a
  defect.
- **Answer marking: majority practice, not a rule.** Boxed answers in 4 of 7
  papers ("Answer to RQ1:" TypeGen; "Summary for RQ3:" commit messages; a
  boxed "RQ4: …" statement in HoarePrompt), bold-italic run-ins in EDEFuzz,
  "Findings:" run-ins in the ICSE'23 study — and *Pinning* marks nothing,
  closing each Results subsection in plain prose. Use a marked answer; it is
  cheap and expected. Do not demand one in review.

## Title

Tools: `ToolName: one-line positioning` or a plain technical statement.
Empirical: the template **"An Empirical Study of X for/on Y"** is safe and
common (ICSE'26 and FSE'25 award lists both contain instances). Equally
accepted, and what the two award-winning empirical papers read here actually
chose, is a **claim hook plus colon**: "Pinning Is Futile: You Need More Than
Local Dependency Versioning…", "The Hidden Cost of Readability: How Code
Formatting Silently Consumes Your LLM Budget".

## Abstract

~150–200 words. Gap → approach → quantified result; confirmed on the FSE
paper (~190 words, closing on "nearly 30%… up to 75%"). Tool papers may claim
"the first X" (with care). Stating the RQ count in the abstract ("We
investigated 6 research questions in three areas") is one paper's habit
(*n=1*), not a field convention — the FSE'25 and ICSE'26 empirical papers
state findings, never a count.

## Introduction

Tool: hook → gap → the key insight set off in italics → 3 contribution
bullets. An early "Research Ethics" subsection appears when disclosure was
involved. Empirical: numbered contributions 1)–5), or a bold run-in
**Summary of Contributions.** paragraph (FSE'25). The honest-scope sentence
is a community idiom worth copying: "This paper does not mean to provide a
complete solution… but is an exploration towards these goals."

## Methodology (empirical studies)

Subject/model selection with explicit bulleted criteria; a reproduction
honesty paragraph (within-2% of original results, exceptions named with
causes); per-RQ Study Setup giving splits, folds, and the statistical model
with its equation; owned bias ("the grouping is subject to bias — two authors
discussed and agreed"). Mining studies report the pipeline's failure rate and
defend it (*Pinning*: 83.6%/87.7% resolution success, failure causes broken
out by percentage, then an argued case that the rate is acceptable).

## Threats to Validity — reality check

Across the seven papers read, **none uses the full internal / external /
construct three-way split**, but the section itself is normal and the
textbook *vocabulary* is now more common than pure prose:

- 4 of 7 carry a labeled ToV section or subsection: HoarePrompt §6 "Threats
  of Validity", *Hidden Cost* §6 with topical subsections ("Generalization",
  "Non-transparent Commercial LLMs"), the commit-message study §7.2 nested
  under Discussion, and the ICSE'23 study's one-paragraph prose ToV.
- Of those, three reach for at least one textbook label — *external validity*
  alone (HoarePrompt), *external* + *internal* (commit messages), or a
  topical heading standing in for it ("Generalization").
- FSE'25 *Pinning* has no ToV section: it distributes bold run-in
  "**Limitations and Threats to Validity.**" paragraphs inside each RQ's
  Method subsection, naming only external validity.
- The two tool papers (EDEFuzz, TypeGen) have none at all, folding
  limitations into Discussion.

Rules to apply: an empirical study needs an explicit ToV discussion (4 of 4
empirical papers have one). A tool paper may fold it into
Discussion/Limitations (2 of 3 do). Naming **external validity** when you
discuss generalizability is the single most common move and costs nothing;
the full three-way split is not expected and should not be demanded.

## Related work

Placement splits roughly evenly and is *not* late-by-default. Early §2 as
"Background and Related Work" (FSE'25 *Pinning*; the ICSE'26 commit-message
study folds it into §2 Background) versus late before Conclusion (EDEFuzz,
HoarePrompt §7, *Hidden Cost* §5). Decide by whether the reader needs a
taxonomy of prior approaches before the method, then commit. Note that FSE
scores "appropriate comparison to related work" as its own review axis, so
thin coverage is a named failure there regardless of placement.

## Tone

"We" throughout; methods in past tense, discussion in present/conditional.
Hedging idioms: "We believe that…", "This suggests that…", "One possibility
is… Another possibility is…" (parallel hypotheses instead of one confident
guess). *Pinning* leans on "we believe" repeatedly inside its ToV paragraphs
to own a judgment call rather than assert it. A closing aphorism in
Discussion is tolerated ("Simple ideas are often the best."). Findings that
cut against expectation are flagged in-line as such ("not only (as
expected)… but also (surprisingly)…").

## Reviewer personas at this venue

- **A — domain expert**: coverage of prior tools/studies on the same
  problem; whether the empirical subjects (datasets, projects) are the
  community-standard ones or a convenience sample. At FSE this is a scored
  axis in its own right.
- **B — rigor / RQ-method alignment hawk**: ICSE's *Rigor* axis —
  "the soundness, clarity, and depth of a technical or theoretical
  contribution, and the level of thoroughness and completeness of an
  evaluation". Do the methods actually answer the stated RQs; are statistics
  appropriate; are reproduction deltas from original papers disclosed.
- **C — verifiability reviewer**: replication package present, complete, and
  actually runnable-looking; enough detail for independent reproduction;
  transparency about manual judgments and their bias. At ASE, check the
  Data Availability Statement exists and sits after the Conclusions.
- **Field must-checks**: page shape matches the *venue*, not the field (FSE
  is single-column acmsmall at 18 pp; ICSE and ASE are 2-column at 10 pp);
  RQ placement matches paper type; Threats-to-Validity present for empirical
  work and honest even if prose-form (the textbook three-way split is *not*
  required — don't demand it); self-scoping statements are a strength, not a
  weakness.
