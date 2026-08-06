---
name: finalize
description: >
  Stage 8 of the paper pipeline: camera-ready checks and the final PDF —
  formatting compliance, anonymization, bibliography hygiene, artifact
  evaluation package. Use after the review loop converges.
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
      "Code is available at …" line added, and the **pipeline
      acknowledgement** (below) included.

## Pipeline acknowledgement (mandatory)

Every paper this pipeline produces credits it in the Acknowledgements —
this is both attribution and the AI-use disclosure that venues
increasingly require (ACM policy puts generative-AI disclosure in the
acknowledgements; NeurIPS asks via the checklist's LLM-usage item; check
the venue's current AI policy for placement and wording constraints).

Canonical sentence, adapted to the venue's register:

> This paper was prepared with \emph{paper-generator}
> (\url{https://github.com/zyx1121/paper-generator}), an LLM-based
> research-paper pipeline; the authors directed the research, approved
> every stage, and verified the results, and all reported numbers come
> from real experiment runs recorded in the project's provenance
> directories.

Placement by review model:

- **Double-blind venues**: the acknowledgement enters at camera-ready
  only (it names a specific tool linked to the authors — treat it like
  any other identity leak at submission). If the venue's checklist or a
  designated disclosure field asks about AI use at submission time,
  answer there truthfully; those channels are anonymity-safe by design.
- **Single-blind / journals**: include it from the first submitted
  version.
- If the venue's AI policy demands a different location (a dedicated
  statement section, the checklist only), follow the venue and keep the
  Acknowledgements credit as well unless the policy forbids it.

## Bibliography hygiene

- Zero undefined citations (the compile report must be clean).
- Consistent venue naming across all entries; arXiv duplicates of published
  papers replaced by the published version; every entry has
  author/title/venue/year.
- Every entry carries a resolvable identifier — DOI or arXiv ID — obtained
  from an index (`dblp_bibtex`, `arxiv_search`), never typed from memory.
  Spot-check that the identifiers of entries added or edited since G5
  actually resolve.
- Confidence is source count: an entry confirmed by two independent sources
  (e.g. DBLP plus the paper's own arXiv page or DOI landing page) is solid;
  an entry only one index knows gets a second look, and a note in the
  delivery summary if it stays single-source.

## Final quality gates

- [ ] Compile clean: no errors, undefined refs = 0, overfull hboxes
      eliminated or < 3pt.
- [ ] Every figure legible at print size (fonts ≥ body-text size when
      placed); vector, fonts embedded.
- [ ] Visual pass: Read the final PDF page by page (the Read tool renders
      PDF pages) — float placement, tables within margins, no orphaned
      headings, nothing colliding. Do this last; it catches what no log can.
- [ ] Title/abstract numbers match the evaluation's numbers exactly.
- [ ] One last lint pass with the banned-word and LLM-tells lists from
      the writing skill's style.md — final edits love to reintroduce them.

## Artifact preparation

Systems, security, and SE venues typically run a separate **artifact
evaluation** (AE) with badges printed on the paper; ML venues instead tie
code release to the reproducibility checklist. Which regime applies comes
from the venue profile and `paper/venue.md`. Then read the venue's **call
for artifacts for the current year**: badge names, deadlines, and
submission mechanics change annually, so nothing here overrides the live
page, and per-venue specifics stay *uncertain* until you have read it.

### The badge vocabulary

ACM's three badge families, adopted with light renaming by USENIX and most
IEEE venues, are independent — a paper can earn one, two, or all three:

| Badge family | Question | What earns it |
|---|---|---|
| Artifacts Available | Can anyone obtain it? | Public, permanent archival deposit with a DOI |
| Artifacts Evaluated (Functional, and at ACM a higher Reusable tier) | Does it run? | Complete, documented, exercisable package |
| Results Reproduced (Replicated when a third party's own artifact is used) | Do the paper's numbers come back? | A reviewer re-obtains the key results |

Available is nearly free once the deposit exists, and is the one badge
worth targeting even when the schedule is tight.

### Process shape

AE is usually a second submission on its own schedule, judged by a
committee separate from the program committee: artifact plus README
uploaded, a short **kick-the-tires** window where reviewers verify only
that the package starts and report blockers, then full evaluation with a
question channel to the authors. Two consequences: the artifact must be
ready weeks after notification rather than months, and a reviewer who
cannot start it during kick-the-tires can sink the badge before reading
any result.

### `paper/artifact/README.md`

The document reviewers actually read. Required parts:

1. **Claims to experiments**, one row per paper claim, in paper order:

   | Claim | Paper location | Script | Runtime | Expected output |
   |---|---|---|---|---|
   | 2.3× throughput over X | §6.2, Fig. 7 | `run_e2e.sh` | ~40 min, 1 node | `fig7.pdf`, ratio within 5% |

   A claim with no row is a claim the artifact does not support. Say so
   explicitly instead of letting a reviewer discover it.
2. **Requirements**, before anything is downloaded: hardware (exact
   GPU/NIC/CPU features, node count, disk), privileges (root, hugepages,
   CPU-governor control), accounts, total disk and compute budget. Special
   hardware is not disqualifying; undeclared special hardware is.
3. **Kick-the-tires path**: one command, small input, under ~10 minutes,
   printing an obviously correct result.
4. **Full reproduction path**: one command per table and figure, plus a
   top-level driver that runs everything in order.
5. **Plotting from data**: the scripts that turn parsed data into the exact
   figures and tables in the paper.
6. **Expected deviation**: which numbers are hardware-sensitive and what
   tolerance still supports the claim. Absolute latencies move across
   machines; a claimed ratio should not.
7. **License** (artifact and data separately if they differ) and how to
   cite.

### Packaging

- Ship an environment, not instructions: a Docker image with a pinned base
  digest, a VM image, or a cloud-ready recipe. Keep the source tree and a
  from-scratch build path beside it so the artifact outlives the image.
- Pin every version, checksum every downloaded dataset, vendor small
  inputs, and assume the network is slow or absent at run time.
- Deposit the released version at an archival host (Zenodo, figshare, or
  the venue's own repository) to obtain a DOI. A bare GitHub URL does not
  earn Artifacts Available; keep the repo as the living mirror and tag the
  exact evaluated commit.
- Provide a reduced-scale configuration for anything longer than a few
  hours, stating which claims it does and does not check.

### Harvest from experiments/, do not rebuild

The package is a reshaping of `paper/experiments/`, not new work: every run
directory already carries its launch command, config and seed, environment
snapshot, untouched raw output, and parsed data. Copy those run scripts
rather than writing fresh ones, so the artifact runs what actually produced
the paper. Ship the raw and parsed data as well, so a reviewer without your
hardware can still re-derive every figure. The Stage 4 rule holds here with
no exceptions: numbers are never regenerated by hand.

### ML venues: release plus checklist alignment

No badge committee, one hard gate — every reproducibility answer in the
checklist must point at something that exists. Release code, seeds, data
splits, full hyperparameters, and the compute actually consumed (hardware
and GPU-hours). A checklist "yes" that the repository does not deliver is
precisely what a reproducibility reviewer hunts for. Supplementary-material
and code deadlines are venue-specific (*uncertain* — check the call).

### Under double-blind

- The artifact link in the paper must be anonymous: an anonymizing
  repository service, an anonymous deposit, or upload through the venue's
  own system. Swap in the permanent link at camera-ready.
- Anonymize the artifact itself, not only the link: author names and emails
  in git history, institution names in paths, hostnames and usernames
  captured in `env.txt`, cluster and account names in configs, internal
  URLs, image labels. Stage 4 records hostnames deliberately, so this
  cleanup always has work to do.
- Grep the whole package for your name, your co-authors', the lab's, and
  the institution's before uploading.

### Checklist

- [ ] Current-year call for artifacts read; badges, deadlines, and
      mechanics recorded in `paper/venue.md`.
- [ ] Target badges decided and stated to the user.
- [ ] `paper/artifact/README.md` complete: claims-to-experiments table,
      requirements, kick-the-tires, full run, expected deviation, license.
- [ ] Kick-the-tires run from a clean checkout in a fresh container,
      following the README literally, with no tacit knowledge applied.
- [ ] Every figure and table in the paper regenerable from shipped data.
- [ ] Environment shipped as an image or fully pinned recipe; datasets
      checksummed.
- [ ] Archival deposit with DOI created (or scheduled for camera-ready),
      and the paper's artifact link points at it.
- [ ] Double-blind: link anonymized, package grepped for identifying
      strings.
- [ ] Anything not releasable (proprietary data, licensed testbed, NDA)
      named in the paper and in the AE submission, with the reason.

## Deliver

Compile the final PDF, place it at `paper/<short-title>.pdf`, update
STATE.md to `done`, and hand the user: the PDF, the page count, the venue's
submission-site reminders (deadline, required fields like conflicts and
topics), the artifact-evaluation deadline and target badges if the venue
has AE, and where everything lives in the workspace.
