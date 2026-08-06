# Security venue profile

> Facts verified: 2026-08-06 — format rules (pages, templates, checklists,
> deadlines-adjacent mechanics) decay yearly; re-verify against the live CFP
> before relying on them.

Venues: IEEE S&P, USENIX Security, CCS, NDSS. Grounded in full reads of five
award papers — Terrapin (USENIX Sec'24 Distinguished, protocol attack),
Adversarial Illusions (USENIX Sec'24 Distinguished, ML attack), BENZENE
(S&P'24 Distinguished, analysis tool), Leaky Apps (CCS'25 Distinguished,
large-scale measurement), OCCUPY+PROBE (NDSS'26 Distinguished,
microarchitectural attack) — plus the CCS 2026 and NDSS 2026 calls for
papers read first-hand at sigsac.org and ndss-symposium.org, and the live
USENIX/S&P CFP and ethics pages. Every format and ethics fact below is
first-hand. Structural claims resting on a single paper at a venue are
marked *uncertain*; they are leads, not rules.

## Format facts

- **USENIX Sec**: 13 pp body + 1 page reserved for the mandatory
  **"Ethics considerations"** and **"Open science"** sections immediately
  before References; refs/appendix free.
- **IEEE S&P**: 13 pp + up to 5 pp refs/appendix (18 total), IEEEtran
  `[conference,compsoc]`; format violations rejected without review.
  Review copies must not contain full CVE identifiers (anonymity).
- **CCS**: **12 pp**, unaltered ACM LaTeX **`sigconf`**, excluding the
  bibliography, well-marked appendices, and supplementary material — but
  "reviewers are not required to read the appendices or any supplementary
  material", so nothing load-bearing goes there. Two appendices sit *after*
  the 12-page body **and after the bibliography**: **"Open Science"**
  (required of every paper, artifact-by-artifact, with an anonymous URL
  repeated in HotCRP) and **"Ethical Considerations"** (required whenever
  the work raises concerns; the CFP says add it if in doubt). Neither
  counts toward the limit. CCS **does not accept SoK or survey papers**.
- **NDSS**: **13 pp**, excluding the "Ethics Considerations" section,
  references, and appendices; mandatory NDSS template, US letter, two
  columns no more than 9.25 in high and 3.5 in wide, Times 10 pt or larger
  with 11 pt or larger line spacing. SoK papers **are** in scope (the
  inverse of CCS), without needing the "SoK:" prefix. A topic-fit
  subcommittee desk-rejects theory or proofs without implementation, and
  papers whose contribution is primarily AI/ML rather than security.

**Where the ethics text goes is the sharpest CCS/NDSS-vs-USENIX split** —
same words, three different homes, and putting it in the wrong one is a
formatting error, not a style preference:

| Venue | Ethics section | Placement | Counts toward limit |
|---|---|---|---|
| USENIX Sec | mandatory, plus Open science | immediately before References | no (1 reserved page) |
| CCS | mandatory if concerns exist; Open Science mandatory always | appendix, after the body **and after the bibliography** | no |
| NDSS | **optional** | immediately before References | no |

ACM `sigconf` also carries obligations USENIX and IEEEtran do not: the CCS
Concepts block, keywords, ACM Reference Format, DOI/ISBN and rights text
must be retained verbatim, and the teaser figure is optional. Both award
papers read here run the acmart/NDSS defaults with no visible tightening.

Desk rejects: space-squeezing tricks (negative `vspace`, `savetrees`,
`titlesec`, changed fonts or margins), stripping the ACM metadata blocks,
failed format checker, and anonymization leaks — CCS names "self-references
with 'we'", funding acknowledgements, and deanonymizing GitHub repositories
explicitly; NDSS rejects double-blind violations without review. NDSS also
caps each author at six submissions per cycle, CCS at seven.

## The paper subtype decides the structure

Five subtypes with different skeletons — pick before outlining:

- **Protocol/crypto attack** (Terrapin): long intro with numbered
  subsections (1.1 background primer, 1.2 attack overview + attacker model,
  1.3 contributions incl. a named "Ethics Consideration and Responsible
  Disclosure" subsection). Related work at §2. No standalone threat-model
  section — it lives inside the intro overview.
- **ML/system attack** (Illusions): conventional short intro; **§3 "Threat
  Model"** after Background, split exactly into Adversary's Goals /
  Adversary's Capabilities (scope limits folded into capabilities). Attack
  sections ordered by capability escalation: white-box → transfer →
  query-based → hybrid.
- **Microarchitectural attack** (OCCUPY+PROBE) *(uncertain — one NDSS
  paper)*: intro ends with contribution bullets plus two bolded run-in
  paragraphs, "Responsible Disclosure." (vendor, date, vendor's verdict) and
  "Availability." (repo URL). §2 Background absorbs related work — there is
  **no standalone Related Work section**. §3 is an Overview triptych:
  Motivation (an experiment showing why prior attacks fail) → **Threat
  Model** → Workflow (numbered phases keyed to a figure). §4 is the
  reverse-engineering chapter, one question per subsection, each closing
  with a boxed **"Observation N."**. §5 evaluates the attack, §6 is a
  standalone real-target case study, §7 Discussion carries Mitigations
  (hardware then software) and Limitations. No ethics section at all.
- **Large-scale measurement** (Leaky Apps) *(uncertain — one CCS paper)*:
  **RQ1–RQn are declared in the Introduction**, one per planned result
  section, not at the top of an Evaluation. §2 is a standalone **"Threat
  Model, ... , and Mitigation"** section before Methodology. There is **no
  Evaluation section**; each result section answers one RQ and closes with
  a boxed **"Takeaways"** that restates the RQ verbatim and answers it in
  three bullets. Related work lands **late** (§9, after Limitations).
  Disclosure appears as a subsection inside each finding chapter, and the
  disclosure email template goes in an appendix.
- **Defense/analysis tool** (BENZENE): systems-paper shape — contribution
  bullets, pipeline-walkthrough design sections, **RQ1–RQ3 stated at the
  top of Evaluation** (RQs are native here, unlike systems venues), related
  work late (after Discussion/Limitations), and possibly no ethics section
  at all when no new vulnerability is disclosed.

**Threat model, refined (n=5).** The old "attack papers put it at §3" rule
was too weak. Corrected: *every paper with an adversary names its threat
model as a titled unit, always before the technical core and never after
the evaluation; only its rank varies.* Illusions and Leaky Apps make it a
top-level section (§3 and §2); OCCUPY+PROBE makes it a subsection of the
Overview section, between Motivation and Workflow; Terrapin folds it into a
numbered intro subsection. The one paper without a named threat model,
BENZENE, is the one with no adversary. So: never omit it from an attack or
measurement paper, and never demand it from an analysis tool.

Content pattern, consistent across all four adversary papers: scenario
first (who runs where, on which shared resource), then capabilities, then
assumptions explicitly inherited from prior work ("Similar to previous BTB
side-channel attacks, we assume …"), then the attacker's objective in one
sentence. OCCUPY+PROBE adds a move worth stealing — a footnote on the
threat model that *relaxes* its strongest assumption and forward-references
the section which removes it, defusing the reviewer's objection at the
point it forms. Measurement papers instead name an established model and
cite it (Leaky Apps: Man-At-The-End), then say what an attacker can obtain.

**Related work has three legal homes**, and the choice is not free: §2 as
its own section (protocol attack), folded into §2 Background with no
separate section (microarchitectural attack), or late after Limitations
(tool and measurement papers). Papers that place it late still open with
two to four intro paragraphs walking the closest prior work and closing on
an explicit "our study differs in three respects" list — the late section
is an expansion, not the first mention.

## Title

Named attacks are brands: `AttackName: mechanism subtitle`. Non-named
attacks: evocative noun phrase + "in <domain>". Tools: invented acronym +
colon + descriptive subtitle, typeset in small caps throughout. Attack
names are typeset in small caps too, in every occurrence including the
title. Measurement papers use a short evocative label + colon + a literal
scope description naming corpus and platforms ("Large-scale Analysis of
Secrets Distributed in Android and iOS Apps"). Venues trim whimsical
preprint subtitles at publication.

## Abstract

170–300 words — longer than ML/systems. Moves (attack): stakes → capability
claim ("we show that X is no longer a secure channel") → mechanism →
real-world impact → measurement numbers → root-cause diagnosis →
mitigation. The microarchitectural variant opens instead on the *gap*
("existing attacks either fail to … or suffer from …") and then claims to
bridge both halves of it, which pre-commits the evaluation to one section
per half. Numbers are always relative with explicit comparators; the
closing sentence hedges (countermeasures, limitations) rather than
declaring victory.

## Evaluation

- Attack papers: "Evaluation" recurs as a subsection inside each attack
  section; a separate internet-measurement section ("X Deployment
  Statistics") gets its own Methodology subtitle.
- Microarchitectural attacks: one Evaluation section whose subsections are
  named after the *claims* rather than the metrics (Experiment Setup, then
  one subsection per capability asserted in the abstract), followed by a
  separate end-to-end case-study section against a real target. Success
  tables are per-device rows × with/without-defense columns, so the
  baseline's collapse under a deployed mitigation is visible in one glance
  (48.9% vs 100%). Any non-obvious accuracy metric gets a displayed
  formula.
- Tool papers: single Evaluation opening with RQs, then subsections named
  Dataset and Setup / Effectiveness / Correctness / Efficiency.
- Measurement papers: no Evaluation section; result sections named after
  the phenomenon. Cross-group differences are reported with a stated null
  hypothesis, a dependent t-test p-value, and a Cohen's d effect size
  inline in the prose ("1.94% vs. 2.83%, p < 0.01, d = −0.04") — a
  statistical bar the attack subtypes do not carry. Illustrative findings
  are named run-in paragraphs, "Case Study: <real product>."
- Success-rate idiom, non-negotiable: headline % + denominator + named
  baseline — "95.6% (44 out of 46 cases), whereas AURORA achieves 63.0%" —
  plus a failure-analysis paragraph naming which cases failed and why.
  Where a mean is quoted, quote its spread with it ("98.6% mean accuracy
  with a standard error of 4.7%").

## Ethics and disclosure

The section is not the deliverable; the evidence is. Neither the CCS nor
the NDSS award paper read here has an ethics section, and both are on
sensitive material — OCCUPY+PROBE carries one bolded intro paragraph naming
the vendor, the report date, and the vendor's verdict; Leaky Apps argues
ethics inside its Methodology (why remote credential validation was safe,
how false positives were filtered to avoid wasting developer time), then
reports disclosure per finding class with counts, dates, bounce rates, and
a table of developer replies coded independently by two researchers.

Calibrate to what was actually done: a live-system 0-day needs dates,
vendor counts, CVE IDs, patch-adoption data, scan opt-out handling
(Terrapin-grade); a research-model attack needs one honest sentence; a tool
over already-published CVEs may need none.

Venue policy, quoted first-hand:

- **USENIX**: disclosure expected at discovery time; undisclosed
  vulnerabilities without justification are grounds for rejection.
- **S&P**: disclosure 45–90 days before publication.
- **CCS 2026**: an "Ethical Considerations" appendix is required for papers
  that raise concerns, and must "discuss the balance of risks vs. benefits
  and the steps taken to minimize potential harm". Note the trap in the
  same paragraph: "institutional (IRB/ERB) approval is neither strictly
  necessary nor always sufficient to demonstrate ethical conduct; we expect
  authors to reason about the ethics of their work beyond ensuring
  institutional compliance." CCS defers its community standard to the
  USENIX Security'26 ethics policy, so the two venues can be prepared from
  one text — only the placement differs.
- **NDSS 2026**: the section is optional, but "Submissions may be rejected
  regardless of scientific merit if they fail to adequately address ethical
  concerns", "IRB exemptions may not be sufficient grounds for proper
  mitigation", and for a "potentially high-impact vulnerability, the
  authors should report or at least discuss their plan for responsible
  disclosure". An Ethics Review Board of TPC members reviews any paper a
  reviewer flags; the Menlo Report is the named reference.

Artifacts are now an ethics-adjacent gate at CCS, not a courtesy: the Open
Science appendix must enumerate every artifact, describe how the PC reaches
it under double-blind review, and justify anything withheld. "If a claimed
contribution depends on an artifact that is not available and not
convincingly justified, reviewers may judge that the contribution cannot be
adequately evaluated" — a rejection route with no equivalent at the other
three venues. Anonymous hosting is required; personal sites, Drive, and
non-anonymized GitHub are called out as unacceptable defaults.

## Tone

"We" + present tense for protocol/system facts, past tense for the
experiment and disclosure timeline. Limitations sections are unusually
candid — named failure categories with case numbers beats generic caveats,
and the microarchitectural paper states its scope limits flatly ("cannot be
extended across SMT threads or physical cores"; "conducted exclusively on
Intel processors") without softening. Signature move: "We identify N root
causes that enable X: First,… Second,…". Inline ①②③ enumeration is
idiomatic in tool papers, and ❶❷❸ callouts keyed to an attack-procedure
figure are idiomatic in attack papers. Bolded run-in paragraph headings
("Attack Description.", "Challenges.", "Result.", "Case Study: X.") carry
most of the fine-grained structure at both ACM and NDSS venues — prefer
them to a fourth level of numbered subsection.

## Reviewer personas at this venue

- **A — domain expert**: hunts whether the "first attack on X" claim
  survives a search, whether the attack surface was already known, and
  whether the defense is bypassed by a published variant. Also owns venue
  fit, which is a real desk-reject route: SoK and survey papers are
  out of scope at CCS but explicitly in scope at NDSS, and NDSS
  pre-filters papers whose contribution is primarily AI/ML, or that are
  theory without implementation on real systems.
- **B — threat-model hawk**: is the adversary model coherent and realistic;
  do the capabilities assumed in the threat model match what the evaluation
  actually grants; are success rates given with denominators and named
  baselines; is the failure analysis case-by-case. Expects the threat model
  to be a titled unit before the technical core whenever there is an
  adversary, and expects inherited assumptions to be attributed to the
  prior work they come from.
- **C — ethics/process reviewer**: disclosure done at discovery time with
  timeline, vendor responses, CVE handling (redacted for anonymity at
  S&P); mandatory Ethics considerations + Open science sections present
  (USENIX); "Ethical Considerations" and "Open Science" appendices placed
  after the bibliography (CCS); human-subjects/IRB status where applicable,
  with the reminder that approval is neither necessary nor sufficient and
  that an IRB exemption is not by itself a mitigation. Undisclosed
  vulnerabilities without justification are grounds for rejection. At NDSS
  this reviewer can escalate to an Ethics Review Board rather than decide
  alone.
- **D — artifact/reproducibility reviewer (CCS)**: reads the Open Science
  appendix as part of the submission and may conclude a contribution cannot
  be evaluated at all. Every claim that rests on an implementation,
  dataset, or benchmark needs a reachable anonymous artifact or a written
  justification for its absence.
- **Field must-checks by subtype**: attack papers — real-world impact
  quantified, responsible-disclosure evidence; measurement papers — the
  RQ declared in the intro must be the one the section answers, and
  cross-group claims need a test statistic and effect size, not just two
  percentages; tool papers — RQs are native here (don't flag), but demand
  the per-case failure table. Do **not** demand a threat-model section from
  an analysis tool with no adversary, and do **not** demand a standalone
  Related Work section: folding it into Background or placing it after
  Limitations are both idiomatic here.
