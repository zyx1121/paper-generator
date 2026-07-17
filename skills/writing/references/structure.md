# CS paper structure reference

Distilled from Simon Peyton Jones ("How to Write a Great Research Paper"),
Jennifer Widom ("Tips for Writing Technical Papers"), the SIGPLAN Empirical
Evaluation Guidelines, and current venue author guides.

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

Widom's hard rule: **a clear new technical contribution must be articulated
by the end of page 3.** Every section tells a story linearly — no backtracking.

ML venues (NeurIPS/ICML/ICLR): single column, 8–9 content pages, Related Work
at Section 2, unlimited appendix, mandatory limitations discussion and
reproducibility checklist.

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

- Describe the problem **with an example**, molehills not mountains.
  Anti-pattern: "Computer programs often have bugs. Many researchers have
  tried to eliminate them [1,2,3]." Pattern: "Consider this program, which
  has an interesting bug. …We show an automatic technique for identifying
  and removing such bugs."
- **Contributions are refutable claims**, bulleted, each with a forward
  reference to the section that substantiates it: "We prove the type system
  sound (§4)." The contribution list drives the entire paper — the paper
  exists to substantiate these claims.
- End with the headline numbers (matching the abstract).
- **No roadmap paragraph** ("The rest of this paper is organized as
  follows…") — the forward references in the contributions already do that
  job. (A one-line roadmap is tolerated at ML venues; skip it elsewhere.)
- One ping per paper: be 100% explicit about the single key idea.

## Design/Method

- Top-down: architecture overview + figure first, so a skimming reader still
  gets the idea; then components in dependency order.
- **Examples before generality.** Introduce the mechanism on the running
  example, then give the general case. Intuition is primary.
- Every design decision that a reviewer could question gets its rationale in
  place ("We chose X over Y because …").

## Evaluation

- Open with explicit research questions: "Our evaluation answers: RQ1 …
  RQ2 …". One subsection per RQ; each ends with a bolded takeaway that
  answers it.
- First subsection is always **Experimental Setup**: hardware, versions,
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
  self-contained caption that states the finding, not just the topic.

## Related Work

- **Late placement** (before Conclusion) by default — SPJ: early related work
  is incomprehensible before the reader knows your idea, and "gets between
  the reader and your idea." Put 1–2 positioning sentences in the intro
  instead. ML convention keeps it at §2; follow venue norms.
- Thematic paragraphs with bold lead-ins ("**Learned indexes.** …"), never a
  paper-by-paper list.
- Every cluster ends with an explicit differentiator: "Unlike X [12], which
  requires offline profiling, we …".
- Be generous with credit — it does not diminish yours, and the authors you
  slight are plausibly your reviewers. Missing the closest prior work is the
  classic desk-reject.

## Conclusion

Short. Restate the contribution now-quantified ("…improves p99 by 2.3× across
three workloads"), one honest limitation, future work in one or two concrete
sentences ("We are currently extending X to Y" marks territory).

## LaTeX conventions

- Templates: `acmart` (`[sigconf]`, `[sigconf,review,anonymous]` for
  submission), `IEEEtran` (`[conference]`), USENIX style file, or the venue's
  ML style file. Use the venue's official copy, current year.
- `booktabs` tables; `subcaption` for subfigures; `\centering`;
  captions below figures, above tables.
- `hyperref` then `cleveref`; `\cref{fig:arch}` everywhere; label prefixes
  `fig: tab: sec: eq: alg:`.
- BibTeX via DBLP entries (the `dblp_bibtex` tool) — consistent venue naming,
  prefer the published version over the arXiv preprint of the same paper,
  complete fields. Never paste random inconsistent entries.
- Double-blind: anonymous author block, own prior work in third person,
  no acknowledgements, anonymized artifact links, scrubbed PDF metadata.

## What reviewers score (bake in from the start)

Soundness (claims backed by evidence), clarity (an expert could reproduce),
significance, novelty/positioning, reproducibility, honest limitations.
NeurIPS explicitly instructs reviewers to *reward* stated limitations.
The standard weaknesses reviewers hunt: missing baseline, unfair tuning,
no error bars, overclaiming ("first ever", "optimal"), missing closest
citation, evaluation that dodges the paper's own claims.
