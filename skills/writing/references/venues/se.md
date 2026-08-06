# Software engineering venue profile

> Facts verified: 2026-08-06 — format rules (pages, templates, checklists,
> deadlines-adjacent mechanics) decay yearly; re-verify against the live CFP
> before relying on them.

Venues: ICSE, FSE, ASE. Grounded in full reads of EDEFuzz (ICSE'24
Distinguished, tool), TypeGen (ASE'23 Distinguished, tool), and an ICSE'23
empirical study on DL vulnerability detection. This is the home of
RQ-driven writing — ICSE's own review criteria define soundness as whether
contributions "address its research questions" via rigorous methods.

## Format facts

- 2-column ACM/IEEE format, 10–12 pp typical (check the year's CFP).
- Review axes (ICSE, verbatim categories): Soundness, Significance,
  Novelty, Verifiability and Transparency, Presentation. Verifiability in
  practice means an open replication package — all three papers ship one.

## Two paper types, two RQ placements

- **Empirical study**: RQs listed in the *Introduction*, grouped by theme,
  each with a rationale sentence. Body section "Research Questions and
  Findings" groups RQs under thematic subsections; every RQ internally runs
  bold run-ins **Motivation → Study Setup → Findings**.
- **Tool/technique**: RQs first appear at the top of *Evaluation*;
  subsection titles can literally be the RQs ("RQ1: Effectiveness of X").

## RQ craft

- 4–6 RQs. Verb moods: Do/Are judgment questions (empirical), How
  effective / What are the impacts (tool). An RQ may embed its own metric
  definition.
- Never a bare question: each RQ is followed by one rationale sentence
  ("This helps us understand…").
- Answer presentation varies — gray "Answer to RQ1:" boxes (TypeGen),
  bold-italic run-ins + prose (EDEFuzz), "Findings:" run-ins (empirical).
  Rule to apply: every RQ unit ends with a visually marked answer
  statement; the box is optional.

## Title

Tools: `ToolName: one-line positioning` or a plain technical statement.
Empirical: the fixed template **"An Empirical Study of X for/on Y"**.

## Abstract

~150–200 words. Gap → approach → quantified result. Tool papers may claim
"the first X" (with care). Empirical studies state the RQ count in the
abstract ("We investigated 6 research questions in three areas") and give
one clause per finding.

## Introduction

Tool: hook → gap → the key insight set off in italics → 3 contribution
bullets. An early "Research Ethics" subsection appears when disclosure was
involved. Empirical: numbered contributions 1)–5); the honest-scope
sentence is a community idiom worth copying: "This paper does not mean to
provide a complete solution… but is an exploration towards these goals."

## Methodology (empirical studies)

Subject/model selection with explicit bulleted criteria; a reproduction
honesty paragraph (within-2% of original results, exceptions named with
causes); per-RQ Study Setup giving splits, folds, and the statistical
model with its equation; owned bias ("the grouping is subject to bias —
two authors discussed and agreed").

## Threats to Validity — reality check

None of the three papers uses the textbook internal/external/construct
split. Tool papers often skip the section entirely in favor of
Discussion/Limitations; the empirical study has a one-paragraph prose ToV.
Write an honest prose ToV covering dataset representativeness and judgment
subjectivity; don't cargo-cult the three-way split (*n=3 — some PCs may
still expect it*).

## Related work

2 of 3 place it late (before Conclusion); the exception merges it with
Background at §2 because the method needs a taxonomy of prior approaches
first. Decide by whether the reader needs the taxonomy, then commit.

## Tone

"We" throughout; methods in past tense, discussion in present/conditional.
Hedging idioms: "We believe that…", "This suggests that…", "One
possibility is… Another possibility is…" (parallel hypotheses instead of
one confident guess). A closing aphorism in Discussion is tolerated
("Simple ideas are often the best.").

## Reviewer personas at this venue

- **A — domain expert**: coverage of prior tools/studies on the same
  problem; whether the empirical subjects (datasets, projects) are the
  community-standard ones or a convenience sample.
- **B — RQ-method alignment hawk**: ICSE's own definition of soundness —
  do the methods rigorously answer the stated RQs; is each RQ followed by
  its rationale and closed with a marked answer; are statistics appropriate
  (and reproduction deltas from original papers disclosed).
- **C — verifiability reviewer**: replication package present, complete,
  and actually runnable-looking; enough detail for independent
  reproduction; transparency about manual judgments and their bias.
- **Field must-checks**: RQ placement matches paper type (intro for
  empirical studies, evaluation for tool papers); Threats-to-Validity
  honest even if prose-form (the textbook three-way split is *not*
  required — don't demand it); self-scoping statements are a strength,
  not a weakness.
