# CS paper structure reference

Distilled from Simon Peyton Jones ("How to Write a Great Research Paper"),
Jennifer Widom ("Tips for Writing Technical Papers"), the SIGPLAN Empirical
Evaluation Guidelines, and current venue author guides.

This file is the generic skeleton. Every field has its own dialect
(evaluation organization, related-work placement, signature sections,
tone); the field profiles live in [venues/](venues/README.md), and the
profile recorded in `paper/venue.md` overrides anything here that
disagrees with it.

## Skeleton and proportions (12-page two-column conference paper)

| Section | Length | Notes |
|---|---|---|
| Abstract | 150–250 words | written last |
| 1 Introduction | 1–1.25 pp | problem + contributions, nothing else |
| 2 Background / Motivation | ~1 pp | only what the reader needs; a running example lives here |
| 3–4 Design / Method | 3–4 pp | overview first, then components |
| Implementation | 0.5–1 pp | from IMPLEMENTATION_NOTES.md |
| 5 Evaluation | 3–4 pp | as long as Design — reviewers live here |
| 6 Related Work | 0.75–1 pp | usually late (see below) |
| 7 Conclusion | 0.25–0.5 pp | no verbatim repetition of abstract/intro |

Widom's rule: a clear new technical contribution must be articulated by
the end of page 3. Every section tells its story linearly, without
backtracking.

Other formats (single-column ML, FSE, HCI, journals) change the page
budget and section order; take those from the venue profile and
`paper/venue.md`.

## Abstract — six moves, in order

1. Context (1 sentence): the setting that makes this matter.
2. Problem (1–2): the specific unsolved problem.
3. Gap (1): why existing approaches fall short.
4. Approach (2–3): "We present NAME, a … that …" — name the key insight.
5. Results with numbers (1–2): "On <benchmarks>, NAME achieves N.N× … over
   <best baseline> while <preserving property>." Numbers are mandatory.
6. Implication (optional 1).

Self-contained: no citations, no undefined acronyms, no forward references.

## Introduction — SPJ discipline

The introduction does exactly two things: **describe the problem** and
**state the contributions**. One page.

- Describe the problem with an example, molehills not mountains.
  Anti-pattern: "Computer programs often have bugs. Many researchers have
  tried to eliminate them [1,2,3]." Pattern: "Consider this program, which
  has an interesting bug. …We show an automatic technique for identifying
  and removing such bugs."
- Contributions are refutable claims, bulleted by default, each with a
  forward reference to the section that substantiates it: "We prove the
  type system sound (§4)." The paper exists to substantiate these claims.
  Bullet form and section pointers vary by field; the profile decides.
- End with the headline numbers (matching the abstract).
- The roadmap paragraph ("The rest of this paper is organized as
  follows…") is venue-gated: omit it at USENIX-tier systems venues and in
  networking, where the forward references do that job; ICDCS-style IEEE
  conferences and Transactions expect one, and ML tolerates a single line.
  Check the profile.
- One ping per paper: be explicit about the single key idea.

## Design/Method

- Top-down: architecture overview + figure first, so a skimming reader still
  gets the idea; then components in dependency order.
- **Examples before generality.** Introduce the mechanism on the running
  example, then give the general case. Intuition is primary.
- Every design decision that a reviewer could question gets its rationale in
  place ("We chose X over Y because …").

## Evaluation

- Organize per the venue profile; this is one of the strongest field
  tells. RQ-numbered subsections are SE dialect (also security tool
  papers); top systems/networking papers organize by
  setup → per-component → end-to-end → ablation instead. The experiment
  *plan* still uses RQs internally (plan.md); whether they surface as
  section headers is the venue's call.
- Either way, each unit of evaluation ends with a visually marked takeaway
  that answers what it set out to test.
- First subsection is Experimental Setup: hardware, versions,
  workloads, baselines and how they were tuned, metrics and why, number of
  runs/seeds and variance reporting.
- SIGPLAN checklist to self-audit: clear claims incl. limitations; principled
  benchmark choice (no cherry-picking); adequate baselines; appropriate
  metrics (tails, not just means); statistical rigor (error bars, ≥5 runs /
  ≥3 seeds, geometric mean for normalized speedups); variability reported;
  setup fully documented.
- Ablations attribute the gain to each novel component; scalability curves
  vary the interesting dimension.
- Every figure/table is referenced from the text, placed `[t]`, with a
  self-contained caption. Whether the caption states the finding or just
  labels the content is field-dependent (networking papers add a takeaway
  line; top systems papers use descriptive labels); the venue profile
  decides.

## Related Work

- Late placement (before Conclusion) by default: SPJ's point is that
  early related work "gets between the reader and your idea". Put 1–2
  positioning sentences in the intro instead. Placement is a field
  convention (HCI early, IEEE-tier systems often §2–3, ML §2 or late by
  dependency, security by subtype); the profile decides.
- Thematic paragraphs with bold lead-ins ("**Learned indexes.** …"), never a
  paper-by-paper list.
- Every cluster ends with an explicit differentiator: "Unlike X [12], which
  requires offline profiling, we …".
- Be generous with credit. Missing the closest prior work is the classic
  desk-reject.

## Conclusion

Short. Restate the contribution now-quantified ("…improves p99 by 2.3× across
three workloads"), one honest limitation, future work in one or two concrete
sentences ("We are currently extending X to Y" marks territory).

## LaTeX conventions

- The venue's official template, current year (e.g. `acmart`
  `[sigconf,review,anonymous]` for submission, `IEEEtran` `[conference]`).
- `booktabs` tables; `subcaption` for subfigures; captions below figures,
  above tables.
- `hyperref` then `cleveref`; `\cref{fig:arch}` everywhere; label prefixes
  `fig: tab: sec: eq: alg:`.
- BibTeX from the `dblp_bibtex` tool: consistent venue naming, the
  published version over the arXiv preprint of the same paper, complete
  fields.
- Double-blind rules: see finalize's compliance sweep.
