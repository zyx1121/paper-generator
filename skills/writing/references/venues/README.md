# Venue profiles

Every research community has its own idea of what a paper looks like — the
applied-linguistics literature calls this genre analysis (Swales' move
analysis; Hyland's disciplinary discourses), and the differences are
systematic, not stylistic noise. A paper that follows the wrong community's
conventions reads as foreign to its reviewers even when the content is sound.

Each file here is a field profile: the structural and rhetorical conventions
of one publication community, distilled from close section-by-section reads
of recent award-level papers plus the venues' own CFPs and reviewer guides.
Claims that rest on thin evidence (n=1, secondhand CFP quotes) are marked
*uncertain* inside the profiles — do not harden those into rules.

## Freshness

A profile mixes two kinds of knowledge with very different half-lives. Trust
them differently.

- **Structural and rhetorical conventions** — section order, related-work
  placement, evaluation organization, tone, figure and caption vocabulary,
  how numbers are phrased. These are community habits; they shift over
  decades, not release cycles. Read them as durable.
- **Hard format facts** — page limits, column counts, template versions and
  classes, checklist items, anonymization rules, artifact-evaluation
  mechanics and deadlines. These change every year, sometimes per edition of
  the same venue. The profile holds a snapshot, dated in the `Facts
  verified:` line under each title.

The authority for every hard format fact is **that year's CFP and author
guide**, never this directory. When the venue is locked at Stage 2, re-verify
the profile's format facts line by line against the live CFP, record the
venue-specific truth in `paper/venue.md`, and report any drift so the profile
can be corrected. A profile whose `Facts verified:` date is more than a year
old should be treated as a lead, not a rule.

## How profiles enter the pipeline

1. **Setup (Stage 2)** — when the venue is chosen, record the matching
   profile file in `paper/venue.md` (e.g. `profile: venues/systems.md`).
   If no profile fits, say so in venue.md and fall back to structure.md
   defaults.
2. **Writing (Stage 6)** — read the chosen profile *after* structure.md;
   where they disagree, **the profile wins**. structure.md is the generic
   skeleton; the profile is the field's dialect.
3. **Review (Stage 7)** — pass the profile path to each reviewer persona so
   they judge against the right community's expectations.

## Profiles

| File | Communities | Use when |
|---|---|---|
| [systems.md](systems.md) | OSDI, SOSP, ATC, EuroSys; ICDCS, IC2E, Middleware | Building/measuring a system: OS, cloud, serving, storage |
| [networking.md](networking.md) | SIGCOMM, NSDI, MobiCom, MobiSys, INFOCOM | Networks, wireless, mobile, measurement studies |
| [ml.md](ml.md) | NeurIPS, ICML, ICLR | Learning methods, models, empirical ML science |
| [security.md](security.md) | IEEE S&P, USENIX Security, CCS, NDSS | Attacks, defenses, security analysis tools |
| [se.md](se.md) | ICSE, FSE, ASE | Software-engineering tools and empirical studies |
| [hci.md](hci.md) | CHI, UIST, CSCW | Interactive systems, user studies, qualitative work |
| [journals.md](journals.md) | Nature/Science; IEEE/ACM Transactions | Journal submissions and conference-to-journal extensions |

## Pipeline scope per field

The profiles above say how a field writes. This table says what the pipeline
can actually produce for that field. The pipeline runs computational
experiments end to end; it cannot recruit participants, obtain IRB approval,
conduct an interview, pay compensation, or hold a disclosure conversation with
a vendor. Where a field's core evidence depends on one of those, the pipeline
hands that step back to the user — it never simulates it.

| Field | Pipeline runs autonomously | Handed back to a human | Out of scope |
|---|---|---|---|
| Systems, networking, ML, SE tool papers | The whole evidence loop: testbed, baselines, benchmarks, training, ablations, analysis | Gate approvals; access to machines, datasets, licenses | — |
| SE empirical with manual labeling / multi-coder | Mining, sampling frame, codebook drafts, agreement statistics, analysis of returned labels | The labeling itself, whenever a claim rests on human coders: real coders, real independent labels, real inter-rater agreement | Model-generated labels presented as a human coder or as a second rater |
| Security | Attacks, defenses, measurement, tooling — on systems the user is authorized to touch | Disclosure for a newly found vulnerability: contacting the vendor, CVE request, embargo. The pipeline drafts the report and the timeline; a human sends it and records the real dates | Unauthorized testing of live third-party systems; a disclosure timeline that did not happen |
| HCI artifact / interactive systems (UIST-style) | Building the system; technical evaluation (latency, accuracy, robustness); study protocol, tasks, and instruments; analysis of data the user returns | Every usability or expert study with real participants: IRB, recruitment, sessions, compensation | Synthetic participants, simulated ratings, invented quotes or N |
| HCI qualitative, CSCW, any human-subjects study | Literature framing; protocol and instrument design; analysis and write-up of data the user collected | All data collection — here it *is* the paper's core evidence, not one section of it | Running the pipeline to a finished paper without real participants |

Two rules follow from the table:

- **Raise it at ideation (Stage 1), not at Stage 4.** If the topic's core
  evidence is human-subjects data, say so before G1 and give the real cost
  (IRB alone is weeks). The user then picks one: run the study themselves on
  their own timeline, narrow the claim to what artifact evidence can carry, or
  move the work to a field where the pipeline can produce the evidence.
- **Partial autonomy is still autonomy.** An out-of-scope step does not kill
  the paper. Do everything on the left of the table, block on the returned
  artifact (labels, session data, disclosure dates), and record the handoff in
  STATE.md under `## Open questions` so a resume does not quietly skip it.

## The five axes that vary most

Encoded per-profile; this table is the orientation map.

| Axis | Systems | Networking | ML | Security | SE | HCI |
|---|---|---|---|---|---|---|
| Columns / body pages | 2-col, 11–12 pp | 2-col, 12 pp | **1-col**, 8–10 pp | 2-col, 13 pp | 2-col, 10–12 pp | 1-col, word-count 5–12k |
| Related work | late (before Concl.) | late | varies §2–§6 | attack: §2; tool: late | varies | **early (after Intro)** |
| Evaluation organized by | setup → components → end-to-end → ablation | micro-bench → end-to-end | dataset/model- or question-named | mirrors design §; tools use RQs | **RQ subsections** | study type (usability / qualitative) |
| Signature section | none | measurement study | checklist + appendix | **Threat Model**, Ethics | **Threats to Validity** | Positionality; (anti-)Implications |
| Numbers rhetoric | rounded multipliers (2–4×) | units + × / % | mixed; tables ± std | % with denominator ("44 of 46") | % vs baselines | N= everywhere |

Two cross-cutting corrections to folklore, found while building these:

- **RQ-numbered evaluations are an SE convention** (institutionalized in
  ICSE's own review criteria), also common in security *tool* papers. Top
  systems/networking papers do not use them — they organize evaluation by
  setup → per-component → end-to-end → ablation. Do not export RQ headers
  to systems venues.
- **Figure captions in top systems papers are descriptive labels, not
  claim sentences** (0 of 3 papers read used claim-captions), while
  networking papers do often add a one-line takeaway. The old
  "caption states the finding" rule is field-dependent.
