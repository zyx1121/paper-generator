---
name: publication
description: >
  Stage 9 of the paper pipeline: everything after the submission goes in —
  rebuttal to real reviews, revision rounds, resubmission after a reject,
  and on acceptance the camera-ready, artifact-evaluation submission, and
  preprint release. Use when a real venue decision or real reviews arrive.
---

# Stage 9 — Publication

The pipeline's simulated reviewers end at G6; this stage handles the real
ones. Entry point: real reviews or a real decision arrive from the venue.
Park here after finalize delivers the submission — STATE.md says
`stage: publication (awaiting decision)` — and act on whichever branch
fires. Real reviews are archived verbatim in `reviews/venue/round-N/`
before anything else touches them: they are the most valuable ground truth
the pipeline ever receives about its own blind spots.

## Branch 1 — Rebuttal / author response

Same ledger discipline as the simulated loop (review skill §2–§4), with
three real-world differences:

- **Length and format are hard limits** — read the venue's response rules
  (word/character caps, markdown vs plain text, whether new results are
  allowed). A response that ignores them reads as carelessness.
- **New experiments during rebuttal**: only if the venue permits citing
  them, and they are real runs under `experiments/` like any other — the
  never-fabricate rule does not relax under deadline pressure.
- **Every promised change is a debt** tracked in the ledger; the
  camera-ready (or the resubmission) must show it paid.

Draft the response, walk the user through contested points with a
recommendation each, and let the user submit it.

## Branch 2 — Revision decision (major/minor)

Venues with revision cycles (Middleware, journals) return named revision
tasks. Treat them as a round ledger: one entry per task, each mapped to
fix / experiment / contest-with-reason. Re-enter earlier stages as needed
(a demanded baseline is Stage 4 work, not new adjectives). Ship the
revised manuscript with a point-by-point change letter mirroring the
ledger. One major revision is usually all you get — do not spend it
partially.

## Branch 3 — Reject

- Harvest first: fold each real-review point into the same
  must-fix/should-fix/contest triage as a simulated round. Points the
  simulated reviewers missed get a note in STATE.md — they are calibration
  data for the review skill's personas.
- Re-venue: update `venue.md` (new venue, new deadline, possibly a new
  profile — re-run the writing deltas if the field tier changes), and
  check the new venue's resubmission and concurrent-submission policies.
- Never resubmit unchanged. Fix what the reviews established, re-run the
  simulated loop once over the revised draft, then finalize for the new
  venue.

## Branch 4 — Accept → camera-ready

Substantive changes are over; this is compliance plus de-anonymization.

1. **Read the camera-ready instructions** (the publication-chair email or
   page): final template options, the new page allowance (often +1–2 pages
   — spend it on reviewer-requested clarifications, not new claims),
   copyright/DOI form (the user signs it), and the deadline.
2. **De-anonymize**: real author block and affiliations; own prior work
   back to first person where it reads better; acknowledgements restored
   — including the mandatory pipeline acknowledgement (finalize
   §Pipeline acknowledgement); artifact links swapped to the permanent
   DOI; PDF metadata now filled in, not scrubbed.
3. **Re-run the finalize quality gates** on the camera-ready: compile
   clean, bibliography hygiene, visual pass, page count under the new
   allowance. No margin tricks now either.
4. **Artifact evaluation**: if the venue runs AE, its deadline is usually
   weeks after notification — submit per finalize §Artifact preparation,
   and track the kick-the-tires window in STATE.md.
5. **Preprint and release**: post the accepted version to arXiv per the
   venue's preprint policy (timing and allowed version differ), flip the
   code repository public at the evaluated tag, and add the "code
   available" line.

## Gate G7

Present the camera-ready PDF with a diff summary against the submitted
version (what the rebuttal promised vs. what changed), the AE submission
status, and the preprint plan. The user approves, signs the copyright
form, and performs the actual uploads — venue accounts and author
attestations are theirs, not the pipeline's. Then STATE.md closes:
`stage: done`, with the DOI and the archive links recorded.
