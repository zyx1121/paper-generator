# Security venue profile

Venues: IEEE S&P, USENIX Security, CCS, NDSS. Grounded in full reads of
Terrapin (USENIX Sec'24 Distinguished, protocol attack), Adversarial
Illusions (USENIX Sec'24 Distinguished, ML attack), BENZENE (S&P'24
Distinguished, analysis tool), plus live USENIX/S&P CFP and ethics pages.
CCS/NDSS conventions are unverified extrapolation (*uncertain*).

## Format facts

- USENIX Sec: 13 pp body + 1 page reserved for the mandatory
  **"Ethics considerations"** and **"Open science"** sections immediately
  before References; refs/appendix free.
- IEEE S&P: 13 pp + up to 5 pp refs/appendix (18 total), IEEEtran
  `[conference,compsoc]`; format violations rejected without review.
  Review copies must not contain full CVE identifiers (anonymity).
- Desk rejects: space-squeezing tricks (margins/fonts/spacing), failed
  format checker, anonymization leaks in figures/appendices/links.

## The paper subtype decides the structure

Three subtypes with different skeletons — pick before outlining:

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
- **Defense/analysis tool** (BENZENE): systems-paper shape — contribution
  bullets, pipeline-walkthrough design sections, **RQ1–RQ3 stated at the
  top of Evaluation** (RQs are native here, unlike systems venues), related
  work late (after Discussion/Limitations), and possibly no ethics section
  at all when no new vulnerability is disclosed.

## Title

Named attacks are brands: `AttackName: mechanism subtitle`. Non-named
attacks: evocative noun phrase + "in <domain>". Tools: invented acronym +
colon + descriptive subtitle, typeset in small caps throughout. Venues trim
whimsical preprint subtitles at publication.

## Abstract

170–300 words — longer than ML/systems. Moves (attack): stakes → capability
claim ("we show that X is no longer a secure channel") → mechanism →
real-world impact → measurement numbers → root-cause diagnosis →
mitigation. Numbers are always relative with explicit comparators; the
closing sentence hedges (countermeasures, limitations) rather than
declaring victory.

## Evaluation

- Attack papers: "Evaluation" recurs as a subsection inside each attack
  section; a separate internet-measurement section ("X Deployment
  Statistics") gets its own Methodology subsection.
- Tool papers: single Evaluation opening with RQs, then subsections named
  Dataset and Setup / Effectiveness / Correctness / Efficiency.
- Success-rate idiom, non-negotiable: headline % + denominator + named
  baseline — "95.6% (44 out of 46 cases), whereas AURORA achieves 63.0%" —
  plus a failure-analysis paragraph naming which cases failed and why.

## Ethics and disclosure

Calibrate to what was actually done: a live-system 0-day needs dates,
vendor counts, CVE IDs, patch-adoption data, scan opt-out handling
(Terrapin-grade); a research-model attack needs one honest sentence; a tool
over already-published CVEs may need none. USENIX expects disclosure at
discovery time — undisclosed vulnerabilities without justification are
grounds for rejection. S&P: disclosure 45–90 days before publication.

## Tone

"We" + present tense for protocol/system facts, past tense for the
experiment and disclosure timeline. Limitations sections are unusually
candid — named failure categories with case numbers beats generic caveats.
Signature move: "We identify N root causes that enable X: First,…
Second,…". Inline ①②③ enumeration is idiomatic in tool papers.

## Reviewer personas at this venue

- **A — domain expert**: hunts whether the "first attack on X" claim
  survives a search, whether the attack surface was already known, and
  whether the defense is bypassed by a published variant.
- **B — threat-model hawk**: is the adversary model coherent and realistic;
  do the capabilities assumed in the threat model match what the evaluation
  actually grants; are success rates given with denominators and named
  baselines; is the failure analysis case-by-case.
- **C — ethics/process reviewer**: disclosure done at discovery time with
  timeline, vendor responses, CVE handling (redacted for anonymity at
  S&P); mandatory Ethics considerations + Open science sections present
  (USENIX); human-subjects/IRB status where applicable. Undisclosed
  vulnerabilities without justification are grounds for rejection.
- **Field must-checks by subtype**: attack papers — real-world impact
  quantified, responsible-disclosure evidence; tool papers — RQs are
  native here (don't flag), but demand the per-case failure table. Do
  **not** demand a threat-model section from an analysis tool with no
  adversary.
