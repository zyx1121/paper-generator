# Phrasebook — attested sentences, by rhetorical move

[style.md](style.md) is a list of things not to write. This file is the
positive half: real sentences from award-level papers, sorted by the move
they perform, so a draft has something to imitate rather than only rules to
avoid.

**Read these for rhythm and shape**, not for wording: where the subject
sits, how early the number lands, how far the verb commits, what the
sentence refuses to claim. Shipping any line here verbatim is plagiarism and
also bad writing — the terminology belongs to another paper. Keep the
skeleton, replace every content word.

Conventions used below:

- Each line carries `(paper, venue — source)`. `venues/*.md` is the field
  profile in [venues/](venues/README.md); "research notes" is the
  2026-08-06 venue reading pass that those profiles were built from.
- **An ellipsis inside a quote is the source's truncation, not the
  paper's.** Those lines are sentence *stems*: the opening is attested, the
  completion is yours. Nothing here was extrapolated into a full sentence
  that no one wrote.
- Fields are mixed inside every move on purpose. Take the line whose field
  matches your venue first; borrow across fields only for shape, and check
  the profile before importing another field's habit.
- Where the evidence names a practice but quotes no sentence, the entry says
  so and is marked *(practice)*.

## Abstract opening — context and stakes

Openings are where field dialect is loudest, and the sources kept them
mostly as stems.

- "We present an extensive experimental evaluation of X" (802.11ad in
  Smartphones, INFOCOM'21 — research notes, networking). Networking
  measurement: the paper announces its own genre in the first clause, then
  enumerates novel aspects "(i)… (ii)…".
- "existing attacks either fail to … or suffer from …" (OCCUPY+PROBE,
  NDSS'26 — venues/security.md). Security: opening on the *gap* rather than
  the stakes pre-commits the evaluation to one section per half of it.
- "we show that X is no longer a secure channel" (Terrapin, USENIX Sec'24 —
  venues/security.md). The capability claim arrives as sentence two, before
  any mechanism.
- "Here we show" (Nature's official move-4 opener, matched move-for-move by
  the 2021 chip-placement paper — venues/journals.md). Journals: the result
  sentence is a fixed phrase, and everything before it is background.
- "Aren't existing solutions good enough?" (ML introduction run-in —
  venues/ml.md). A question as a run-in heading is legitimate at ML venues
  and reads as foreign at systems venues.

## System or method declaration

- "This paper presents ServerlessLLM, ..." (ServerlessLLM, OSDI'24 —
  research notes, systems). The system-first abstract: name in sentence one,
  three contribution parts listed inline, headline number last.
- "This paper presents X, a … that …" (system-first abstract opening,
  USENIX tier — venues/systems.md). The alternative is problem-first; both
  are attested, and mixing them reads as indecision.
- "28 GHz testbed with 400 MHz bandwidth, 64-element phased array"
  (mmReliable, SIGCOMM'21 — venues/networking.md). Wireless declares the
  implementation with hardware numbers *inside the abstract*; the same
  sentence in a systems abstract would be an odd use of the budget.
- "we present/discuss N themes/contributions" (near-verbatim idiom across
  four HCI award papers — venues/hci.md). HCI counts its deliverables in
  the abstract.

## Key observation

- "We observe that …" (ServerlessLLM, OSDI'24 — venues/systems.md). The
  hinge paragraph of a systems introduction: one observation, stated as
  observed rather than proved, carrying the whole design.
- "Upon closer inspection of the traces, we noticed... By inspecting packet
  traces... we found that PSM implementation is responsible." (802.11ad in
  Smartphones, INFOCOM'21 — research notes, networking). The measurement
  loop in one sentence: surprising number, raw evidence, named mechanism.
- "From their feedback, we identified four primary categories of
  augmentation techniques." (Augmented Physics, UIST'24 — research notes,
  hci). The formative-study conversion sentence, and the count is exact.
- "We identify N root causes that enable X: First,… Second,…" (security
  award corpus — venues/security.md). Root causes are counted and then
  enumerated in the same breath.
- *(practice)* Microarchitectural attack papers close each
  reverse-engineering subsection with a boxed "Observation N."
  (OCCUPY+PROBE, NDSS'26 — venues/security.md), so a skimming reviewer
  collects the findings without reading the analysis.

## Contribution bullets

Verb-first, parallel, and countable. Do not pad the list to reach four.

- "We identify... / We propose... / We design and implement... / We
  evaluate..." (vLLM, SOSP'23 — research notes, systems). Four bullets, four
  verbs, escalating from problem to evidence.
- "Identify … / Design … / Conduct …" (DistServe, OSDI'24 —
  venues/systems.md). Same ladder with the "We" dropped; a section pointer
  per bullet is optional and this paper carries none.
- "Our research presents several contributions to HCI. Firstly… Secondly…
  Thirdly…" (The Benefits of Prosociality towards AI Agents, CHI'25 —
  venues/hci.md). HCI narrates its contributions in full sentences, and
  qualitative papers repeat them verbatim in the conclusion.
- `Power consumption (§IV): …` (INFOCOM measurement paper —
  venues/networking.md). Bold lead-in plus a section pointer: the
  contribution list doubles as a table of contents.
- "Summary of Contributions." (Pinning Is Futile, FSE'25 — venues/se.md).
  A bold run-in paragraph instead of bullets, which is normal in SE
  empirical work.

## Design opening and roadmap

- "We first show… Then, we derive… We show that…" (mmReliable, SIGCOMM'21 —
  venues/networking.md). The design section opens by naming its own
  subsection order in one sentence.
- "How does PRED perform in practice…? Why does PRED achieve high
  performance?" (PRED, NSDI'25 — venues/networking.md). A bulleted question
  list opening the evaluation is legitimate here; naming the *subsections*
  RQ1/RQ2 is not.
- "How well can DPO optimize the RLHF objective?" (DPO, NeurIPS'23 —
  venues/ml.md). Question-driven experiment subsection titles, the ML
  alternative to dataset-driven ones.
- "The remainder of this paper is organized as follows…" (Tangram, ICDCS'24
  — venues/systems.md). **Venue-gated:** write it for ICDCS and the IEEE
  tier, omit it at OSDI and the USENIX tier, where no paper read carries
  one.
- "Section 8 describes related works and Section 9 concludes this paper."
  (TPDS paper — venues/journals.md). Transactions expect the roadmap
  sentence that USENIX venues delete.

## Claim-first evaluation

State the result, then walk the figure. Every one of these names its
comparator; none of them says "significant".

- "vLLM sustains 1.7×-2.7× higher request rates" (vLLM, SOSP'23 — research
  notes, systems), narrated *before* the figure is discussed; the profile
  records the same move with the baseline named, "X sustains 1.7–2.7×
  higher rates than Orca" (venues/systems.md).
- "can serve 7.4× more requests or 12.6× tighter SLO" (DistServe, OSDI'24,
  published abstract — venues/systems.md). Rounded multipliers are the
  USENIX-tier number style; two-decimal percentages read as IEEE tier.
- "95.6% (44 out of 46 cases), whereas AURORA achieves 63.0%" (BENZENE,
  S&P'24 — venues/security.md). The security success-rate idiom is
  non-negotiable: headline percentage, denominator, named baseline.
- "1.94% vs. 2.83%, p < 0.01, d = −0.04" (Leaky Apps, CCS'25 —
  venues/security.md). Measurement papers carry a test statistic and an
  effect size inline; two bare percentages are a reviewer kill here.
- "H(2) = 16.84, p < 0.001" and "F(2, 291) = 4.50, p < 0.05" (The Benefits
  of Prosociality towards AI Agents, CHI'25 — venues/hci.md). HCI reports M
  and SD for both sides of a comparison before the statistic.

## Differentiator

Every related-work cluster ends on one of these, and it names the single
closest system rather than a family.

- "However/Unlike [prior], [OurSystem] [does X]." (systems related-work
  template — research notes, systems). The default closing sentence of a
  thematic paragraph.
- "DistServe is orthogonal to …" and "DistServe adopts a similar concept
  but …" (DistServe, OSDI'24 — venues/systems.md). State the relationship,
  complementary or superseding, rather than implying superiority.
- "In contrast to X, we…" (mmReliable, SIGCOMM'21 — venues/networking.md).
  Against the closest prior work, networking enumerates the delta
  "(i)… (ii)… (iii)…" instead of asserting it once.
- "our study differs in three respects" (security papers that place related
  work late — venues/security.md). The count comes first; the late section
  is an expansion of this list, not its first mention.
- "Similar to previous BTB side-channel attacks, we assume …"
  (OCCUPY+PROBE, NDSS'26 — venues/security.md). Inherited assumptions are
  attributed to the work they come from, which is a differentiator in
  reverse.

## Takeaway and finding

- "mmReliable has a low probing overhead compared to vanilla 5G NR"
  (mmReliable, SIGCOMM'21 — venues/networking.md). A one-line takeaway
  appended to a descriptive caption: a wireless and measurement habit, and
  wrong at systems venues, where captions are labels.
- "These results supported hypothesis H1(d) but did not support H1(a),
  H1(b), or H1(c)" (The Benefits of Prosociality towards AI Agents, CHI'25
  — venues/hci.md). Nulls stated as plainly as the positive result, in the
  same sentence.
- "we hope our findings inspire and frame questions" (Infrastructuring
  Care, CHI'23 — research notes, hci). The post-Dourish qualitative close:
  a research agenda instead of a design-implications list.
- "Simple ideas are often the best." (SE tool paper, ICSE/ASE —
  venues/se.md). A closing aphorism is tolerated in an SE discussion
  section and nowhere near an evaluation.
- *(practice)* Measurement security papers close each result section with a
  boxed "Takeaways" that restates the research question verbatim and
  answers it in three bullets (Leaky Apps, CCS'25 — venues/security.md); SE
  marks the same move with "Answer to RQ1:" or "Findings:" run-ins
  (TypeGen, ASE'23 — venues/se.md).

## Honest limitations

Reviewers are instructed to reward these at ML, HCI and MobiCom, and to
punish their absence at SIGCOMM. Name the failure; do not hedge it.

- "This paper does not mean to provide a complete solution… but is an
  exploration towards these goals." (empirical study, ICSE'23 —
  venues/se.md). The honest-scope sentence, placed in the introduction
  where it disarms the objection before it forms.
- "cannot be extended across SMT threads or physical cores" and "conducted
  exclusively on Intel processors" (OCCUPY+PROBE, NDSS'26 —
  venues/security.md). Scope limits stated flatly, with no softening verb
  anywhere in either clause.
- *(practice)* BENZENE (S&P'24 — research notes, security) lists six named
  failure categories in its limitations section and identifies the failing
  cases by number. Named failure categories with case numbers beat generic
  caveats; this is the move to copy when an evaluation has misses.
- "the grouping is subject to bias — two authors discussed and agreed"
  (empirical study, ICSE'23 — venues/se.md). Own the manual judgment and
  say how disagreement was resolved.
- "creating fake scenarios where AI agents appear to need help, but
  actually do not, may undermine people's trust" (The Benefits of
  Prosociality towards AI Agents, CHI'25 — venues/hci.md). Each design
  implication is paired with its own ethical limit.

## Hedging, by field

Hedging is field-specific and the mistake is uniform application. One
calibrated hedge per claim; never stack two.

- **ML** — "suggests that", "may", "to our surprise", "speculatively"
  (venues/ml.md, research notes, ml). Debunking papers may take a
  combative register, "we call into question…"; method papers may not.
- **SE** — "We believe that…", "This suggests that…", and the parallel
  hypothesis pair "One possibility is… Another possibility is…"
  (venues/se.md). The pair is the field's way of refusing to guess with
  confidence. Counter-expectation findings are flagged in line: "not only
  (as expected)… but also (surprisingly)…".
- **Systems** — hedging appears only when introducing an empirical
  observation ("We observe that …"); design claims are stated flatly, with
  no "may" or "could" (venues/systems.md, research notes, systems).
- **Networking** — hedging is confined to the discussion, future work, and
  the abstract's final sentence, never scattered through design or
  evaluation. The working verb set is demonstrate, observe, confirm,
  identify, reveal, achieve (venues/networking.md).
- **Security** — the limitations section is candid and unhedged; the hedge
  lives instead in the abstract's closing move, which discusses
  countermeasures rather than declaring victory (venues/security.md).

## Self-declared delta — extensions and rebuttals

- "In this article, we significantly improve and generalize [26], in
  several ways: (a)... (b)... (c)..." (ToN 2024 multicommodity-flow paper —
  research notes, journals). The idiomatic in-paper answer to "what is new
  since the conference version".
- "sketched in our previous short paper [10], however, without any
  technical details, proofs or evaluations" (ToN 2024 — research notes,
  journals). Name what the earlier paper lacked; that is the delta, and
  vagueness here is read as a union of prior publications.
- *(practice)* TPDS requires the submission to answer three questions
  explicitly: the novel contributions beyond the previous publication, what
  the new content is and which sections hold it, and how those
  contributions build on the published material (venues/journals.md). A
  "Novelty and Related Work" subsection is where they go.
- *(practice)* Transactions introductions carry lettered subsections — "A.
  Our Contributions", "B. Novelty and Related Work", "C. Organization"
  (ToN papers — venues/journals.md) — so the delta has a titled home rather
  than being buried in prose.

## How to use one

1. **One line per move, from your field first.** Pick the entry whose venue
   matches `paper/venue.md`; if the field has no entry for that move, take
   the closest one and check the profile before importing its habit. Do not
   assemble a paragraph out of five borrowed skeletons.
2. **Rewrite to the profile's tone.** The same claim is a rounded
   multiplier at OSDI, a two-decimal percentage at ICDCS, a percentage with
   a denominator at S&P, and M/SD plus a test statistic at CHI. The move
   survives the translation; the number rhetoric does not.
3. **Swap in your own terminology, then keep it.** Every content word from
   the quoted line has to go. One term per concept for the whole paper
   (see [style.md](style.md)) — a phrasebook line is the one place a
   synonym is likely to sneak in.
4. **Check the result against style.md, not against this file.** Attested
   does not mean clean: these lines come from real papers, some of them
   non-native, and where an idiom here collides with the ban list, the ban
   list wins.
5. **Never ship a line verbatim.** If the rewritten sentence still matches
   its source on more than a few consecutive words, rewrite it again.
