---
name: writing
description: >
  Stage 6 of the paper pipeline: write the full LaTeX manuscript from the
  proposal, results, and figures — correct structure, professional academic
  prose, real citations, compiled and within the page limit. Use after
  analysis, or when revisions require rewriting sections.
---

# Stage 6 — Writing

Goal: a complete, compiled draft PDF in `paper/manuscript/` that passes gate
G5 and enters the review loop.

**Before writing anything, read the references in full:**

- [references/structure.md](references/structure.md) — what goes where, and
  the per-section formulas (abstract's six moves, SPJ's intro discipline,
  RQ-driven evaluation, late related work).
- [references/style.md](references/style.md) — the prose rules: active
  voice, given-new flow, consistent terminology, claims calibration, banned
  words, and the reads-as-LLM tells to counter-program.
- [references/diagrams.md](references/diagrams.md) — the drawn figures
  (architecture, state, flow): TikZ standalone workflow, style rules, and
  the compile-and-look loop.

## Order of writing

Write in this order — each step feeds the next:

1. **Contributions list** — lift the refutable claims from `proposal.md`,
   updated to what the data in `experiments/results.md` actually supports.
   These bullets drive the whole paper; if a claim lacks evidence, it does
   not get written down, full stop.
2. **Figures and tables placement** — decide which figure/table carries each
   claim, and the headline Figure 1. The paper is written around them.
   Drawn figures (architecture, state, flow) are produced now, per
   references/diagrams.md — Figure 1 is often one of them.
3. **Evaluation** — closest to the data, so write it while the analysis is
   fresh. RQ subsections, setup first, takeaways bolded. Every number
   copied from `experiments/`, never from memory.
4. **Design/Method, then Implementation** (from IMPLEMENTATION_NOTES.md),
   then Background — introduce the running example early.
5. **Related Work** — build `refs.bib` with `dblp_bibtex` (prefer published
   versions over arXiv duplicates; complete, consistent entries). Never
   hand-write a bib entry from memory — if no index (`dblp_bibtex`,
   `arxiv_search`, `scholar_search`) can produce it, do not cite it.
   Thematic paragraphs, each ending with an explicit differentiator.
   Describe a prior work only from material actually fetched and read —
   this session, or the novelty-scan notes in `proposal.md`. Caught
   describing a paper from memory: stop, fetch it, or write
   `[MATERIAL GAP: <paper, what is unknown>]` in the draft and resolve it
   before the gate.
6. **Introduction** — problem-by-example plus the contributions list with
   forward references. One page.
7. **Conclusion**, then **Abstract** (six moves, numbers included) and
   **Title** last.

## Mechanics

- One file per section under `sections/`, `\input` from `main.tex`.
- Compile with `latex_compile` after every section — never let errors pile
  up. Fix undefined references and citations as they appear; the tool
  reports them structured.
- Respect `venue.md`: page limit (check the reported page count on every
  compile), anonymization if double-blind (third person for own prior work,
  no acknowledgements, scrubbed metadata), citation style.
- `\cref` for all cross-references; labels `fig:/tab:/sec:/eq:`.

## Self-check before the gate

Run the revision passes from style.md §Revision passes. Then verify:

- [ ] every contribution bullet forward-references a section that
      substantiates it, and that section actually does
- [ ] every figure/table referenced in text, captions state the finding
- [ ] every number in the text traces to `experiments/`
- [ ] no undefined refs/citations, no compile errors, overfull boxes < 5
- [ ] within page limit with references handled per venue rules
- [ ] terminology grep: no synonym drift on key terms
- [ ] no `[MATERIAL GAP]` markers remain; every prior-work description
      traces to a fetched source
- [ ] **visual pass**: Read the compiled PDF page by page (the Read tool
      renders PDF pages) — float placement, figure sizing and label
      legibility, tables inside the column, no stray page breaks. The
      compile log cannot catch these; eyes can.

Optionally spawn the `copyeditor` agent for an independent prose pass over
`sections/` before presenting the draft.

## Gate G5

Deliver the compiled PDF to the user with a two-paragraph cover note: what
the paper claims, and where you think it is weakest (the review loop will
find it anyway). On approval, the pipeline enters the review loop.
