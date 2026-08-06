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
