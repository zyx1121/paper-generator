---
name: finalize
description: >
  Stage 8 of the paper pipeline: camera-ready checks and the final PDF —
  formatting compliance, anonymization, bibliography hygiene, artifact
  README. Use after the review loop converges.
---

# Stage 8 — Finalize

Goal: a submission-ready PDF and a clean workspace. This stage is a
checklist, not a rewrite — substantive changes reopen the review loop.

## Compliance sweep (against venue.md)

- [ ] Page limit: `latex_compile` page count vs. the venue rule (references
      in or out of the limit, per venue). No margin/font tricks, ever.
- [ ] Correct template and options (e.g. `[sigconf,review,anonymous]` for
      submission vs. camera-ready options).
- [ ] **If double-blind:** author block anonymous; own prior work in third
      person; no acknowledgements; artifact links anonymized; PDF metadata
      scrubbed (`\hypersetup{pdfauthor={},pdftitle={...}}`); no
      institution-identifying names in text, figures, or dataset paths.
- [ ] If camera-ready: authors/affiliations/acknowledgements restored,
      "Code is available at …" line added.

## Bibliography hygiene

- Zero undefined citations (the compile report must be clean).
- Consistent venue naming across all entries; arXiv duplicates of published
  papers replaced by the published version; every entry has
  author/title/venue/year.

## Final quality gates

- [ ] Compile clean: no errors, undefined refs = 0, overfull hboxes
      eliminated or < 3pt.
- [ ] Every figure legible at print size (fonts ≥ body-text size when
      placed); vector, fonts embedded.
- [ ] Title/abstract numbers match the evaluation's numbers exactly.
- [ ] One last lint pass with the banned-word and LLM-tells lists from
      the writing skill's style.md — final edits love to reintroduce them.

## Artifact package (if the venue has artifact evaluation)

Assemble `paper/artifact/README.md`: claims → experiment mapping,
one-command run scripts, environment requirements, expected runtimes.
The `experiments/` provenance directories make this nearly free.

## Deliver

Compile the final PDF, place it at `paper/<short-title>.pdf`, update
STATE.md to `done`, and hand the user: the PDF, the page count, the venue's
submission-site reminders (deadline, required fields like conflicts and
topics), and where everything lives in the workspace.
