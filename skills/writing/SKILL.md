---
name: writing
description: >
  Stage 6 of the paper pipeline: write the full LaTeX manuscript in the
  target venue's conventions, from the proposal, results, and figures. Use
  after analysis, or when revisions require rewriting sections.
---

# Stage 6: Writing

Goal: a complete, compiled draft PDF in `paper/manuscript/` that passes gate
G5 and enters the review loop.

Before writing, read the references in full, in this order:

1. [references/structure.md](references/structure.md): the generic
   skeleton and per-section formulas.
2. The venue profile named in `paper/venue.md` (from
   [references/venues/](references/venues/README.md)): the field's
   dialect (evaluation organization, related-work placement, signature
   sections, abstract length and number style, tone). Where it disagrees
   with structure.md, the profile wins.
3. [references/phrasebook.md](references/phrasebook.md): attested sentences
   from award-level papers, grouped by rhetorical move. Pick the line
   matching the venue's field, keep the shape, replace the words.
4. [references/style.md](references/style.md): the prose rules, banned
   words, and reads-as-LLM tells. style.md rules the final prose.

[references/diagrams.md](references/diagrams.md) covers the drawn figures
(architecture, state, flow): TikZ workflow, style rules, and each field's
figure vocabulary.

## Order of writing

Write in this order; each step feeds the next:

1. Contributions list: lift the refutable claims from `proposal.md`,
   updated to what the data in `experiments/results.md` actually supports.
   A claim without evidence does not get written down.
2. Figures and tables placement: decide which figure/table carries each
   claim, and the headline Figure 1. Produce the drawn figures now, per
   references/diagrams.md; Figure 1 is often one of them.
3. Evaluation, while the analysis is fresh. Setup first, organization per
   the venue profile (RQ subsections only where the field uses them),
   takeaways visually marked. Every number copied from `experiments/`,
   never from memory.
4. Design/Method, then Implementation (from IMPLEMENTATION_NOTES.md), then
   Background; introduce the running example early.
5. Related Work. Build `refs.bib` with `dblp_bibtex` (published versions
   over arXiv duplicates; complete, consistent entries). Never hand-write a
   bib entry from memory: if no index (`dblp_bibtex`, `arxiv_search`,
   `scholar_search`) can produce it, do not cite it. Describe a prior work
   only from material actually fetched and read, this session or in the
   novelty-scan notes in `proposal.md`. Caught describing a paper from
   memory: stop, fetch it, or write
   `[MATERIAL GAP: <paper, what is unknown>]` in the draft and resolve it
   before the gate.
6. Introduction: problem-by-example plus the contributions list with
   forward references.
7. Conclusion, then Abstract, and Title last.

## Mechanics

- One file per section under `sections/`, `\input` from `main.tex`.
- Compile with `latex_compile` after every section and fix undefined
  references and citations as they appear; the tool reports them
  structured.
- Respect `venue.md`: page limit (check the reported page count on every
  compile), anonymization if double-blind (finalize's compliance sweep has
  the list), citation style.
- Acknowledgements: every paper from this pipeline credits it; the
  canonical sentence and the AI-disclosure rationale live in the finalize
  skill (§Pipeline acknowledgement). Single-blind or journal venue: write
  the Acknowledgements now, credit included. Double-blind: leave
  acknowledgements out entirely; finalize adds the credit at camera-ready.
- `\cref` for all cross-references; labels `fig:/tab:/sec:/eq:/alg:`.

## Self-check before the gate

Run the revision passes from style.md §Revision passes. Then verify:

- [ ] every contribution bullet forward-references a section that
      substantiates it, and that section actually does
- [ ] every figure/table referenced in text; captions follow the venue
      profile's convention (descriptive label, or label plus finding)
- [ ] **after any compression pass** (abstract cut, bullet merge, section
      shortening): re-verify every surviving number and qualifier against
      the fuller statement it replaced. Compression is how ranges collapse
      onto their most favorable endpoint and scope qualifiers ("at low
      concurrency") silently vanish; a live restyle introduced exactly
      these two errors into an abstract that three review rounds had
      already vetted
- [ ] every number in the text traces to `experiments/`: run `trace_check`
      (manuscript dir vs. `experiments/`) and account for every unmatched
      value it flags: point it at the evidence, mark it as derived/quoted,
      or delete it
- [ ] no undefined refs/citations, no compile errors, overfull boxes < 5
- [ ] within page limit with references handled per venue rules
- [ ] run `style_lint` (manuscript dir + the paper's key terms) and judge
      every finding: fix it, or note why it stays ("the very X" and
      predicate "in flight" are legitimate English the lint cannot know)
- [ ] terminology grep: no synonym drift on key terms beyond what
      `style_lint` already flagged
- [ ] no `[MATERIAL GAP]` markers remain; every prior-work description
      traces to a fetched source
- [ ] visual pass: Read the compiled PDF page by page (the Read tool
      renders PDF pages) for float placement, figure sizing and label
      legibility, tables inside the column, stray page breaks. The compile
      log cannot catch these.

Optionally spawn the `copyeditor` agent for an independent prose pass over
`sections/` before presenting the draft.

## Gate G5

Deliver the compiled PDF to the user with a two-paragraph cover note: what
the paper claims, and where you think it is weakest (the review loop will
find it anyway). On approval, the pipeline enters the review loop.
