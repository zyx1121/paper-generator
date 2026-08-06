# Networking / wireless / mobile venue profile

> Facts verified: 2026-08-06 — format rules (pages, templates, checklists,
> deadlines-adjacent mechanics) decay yearly; re-verify against the live CFP
> before relying on them.

Venues: SIGCOMM, NSDI, MobiCom, MobiSys, INFOCOM. Grounded in full reads of
mmReliable (SIGCOMM'21), Gemini (MobiCom'24), an INFOCOM'21 WiGig
measurement study, and PRED (NSDI'25, datacenter RED/ECN tuning on a Tofino
switch) as the wired-core control. Format facts come from the venues' own
2025/2026 CFPs and submission pages; reviewer-culture facts from the SIGCOMM
author guide and the MobiCom/MobiSys CFPs. Sources listed at the end.

## Format facts

Every number below is from the venue's own submission page, read 2026-08-06.
Page geometry is near-identical across the three ACM venues; what actually
differs is the page *budget* and the review machinery.

- **SIGCOMM '26**: body ≤ 12 single-spaced pages, everything before
  references and appendices, figures and tables included. Longer body: not
  reviewed. References and appendices are unlimited, but reviewers need not
  read them and main-body claims may not depend on appendix experiments.
  Two-column, each column 9.25" × 3.33", 0.33" gutter, ≥ 10-point font,
  ≤ 55 lines per column, US Letter. Abstract ≤ 200 words. A statement on
  ethical considerations is mandatory in the body (the sentence "This work
  does not raise any ethical issues" satisfies it); omitting it can get the
  paper rejected. Double-blind. An automated format checker runs after the
  deadline and PC chairs manually inspect and may reject evident violations.
  New in 2026: authors upload their `.bbl` so references can be validated
  against hallucinated GenAI citations.
- **NSDI '26**: ≤ 12 pages including footnotes, figures and tables;
  references and appendices unlimited. Two-column, 10-point type on 12-point
  leading, 7" × 9" text block, 0.33" gutter. Papers that miss these criteria
  are rejected without review, with no extension to reformat. Double-blind,
  except an operational-systems track reviewed under a deliberately weaker
  double-blind (names withheld, but company and system names may stay).
  Decisions are accept / reject / one-shot revision.
- **MobiCom '26**: ≤ 12 pages of non-bibliographic content; appendices sit
  after the references and are free. Same ACM geometry as SIGCOMM
  (≥ 10 pt, 9.25" × 3.33", 0.33", ≤ 55 lines); template is
  `\documentclass[sigconf,10pt]{acmart}`. Double-blind, and a double-blind
  violation means the paper is not reviewed. A placeholder title or abstract
  ("TBD") at abstract registration is a desk reject; the registered abstract
  must run ≥ 100 meaningful words.
- **MobiSys '26**: same geometry and same 12-page main-content rule, but
  **single-blind as of 2026** — the CFP reverts the 2017 anonymity policy
  and now *requires* names, affiliations and contact details on the
  manuscript. Undeclared LLM-generated text is a desk reject; text an LLM
  merely proofread is exempt. Human-subjects work without an ethics-board
  certification is rejected.
- **INFOCOM '26**: ≤ 10 printed pages *total*, of which the main text
  (figures, tables, appendices, everything except the references) is ≤ 9.
  Over-length papers are not reviewed. Unmodified `IEEEtran.cls` v1.8 with
  `\documentclass[10pt, conference, letterpaper]{IEEEtran}`, 10-point Times,
  two-column; overriding line spacing, font size, margins or column gap is
  explicitly prohibited. Double-blind, enforced hard: non-conforming
  anonymization, a PDF that is not text-searchable, or author identity left
  in the PDF metadata each get the paper rejected or returned without
  review. The submission must be self-contained — no anonymous technical
  report, no Dropbox/OneDrive appendix, and the paper may not even *refer*
  to an extended report. Abstract ≤ 200 words in the EDAS metadata. An
  author may appear on at most five submissions; the sixth onward is
  rejected without review.

**INFOCOM is an IEEE-type venue and that changes what you write, not just
how you format it.** Its references eat the page budget (9 pages of content
inside a 10-page file), the appendix escape hatch is closed by policy, and
the 2026 guidelines describe no rebuttal or revision round at all: one
submission, one decision. The ACM/USENIX-type venues (SIGCOMM, NSDI,
MobiCom, MobiSys) give free references plus appendices, run rebuttals or
one-shot-revision loops, and add ethics and artifact machinery. Practical
consequence: for INFOCOM, cut until the argument is complete in 9
self-contained pages and cite sparingly; for SIGCOMM/NSDI, keep the body
self-contained but push overflow into appendices reviewers are free to skip.

Figure-heavy culture regardless of venue: 10–16 figures on 10–15 pages;
tables only for compact numeric grids (device × metric).

## Title

- System papers: metaphor/slogan + colon + property claim ("Two beams are
  better than one: Towards Reliable and High Throughput mmWave Links") or
  plain `Name: function`.
- Measurement papers: "`Tech` in `Platform`: Axis1, Axis2, and Axis3" —
  the title previews the results sections one-to-one.

## Abstract

~7 sentences, ~150 words. System move order: context → gap → system name +
mechanism (2 sentences) → why it works → implementation with hardware
numbers ("28 GHz testbed with 400 MHz bandwidth, 64-element phased array")
→ quantified headline. Measurement papers open "We present an extensive
experimental evaluation of X", enumerate novel aspects "(i)… (ii)…", close
with a hedged future-work pointer. Numbers always carry units and a
comparator (2.3×, close to 100%); "significant" without a number is banned.

## Introduction

Funnel: field-promise paragraph (cite the standard/spec) → specific gap →
for measurement papers, an enumerated list "(i)–(iv)" of why prior findings
don't transfer. Figure 1 in the wireless papers is a two-panel schematic:
"(a) Conventional [failure] (b) OurSystem [success]". The wired-core
alternative is a design-space map that places the new system among the
existing families and marks the path to it (PRED's Figure 1, "Design space
in Datacenters"); use it when the contribution is a position rather than a
mechanism swap. Contribution style splits by sub-venue:
INFOCOM/measurement papers use bolded lead-ins with section pointers
("Power consumption (§IV): …" — contributions as a table of contents);
MobiCom uses plain bullets; SIGCOMM system papers may state contributions in
flowing prose with no bullets at all. No roadmap paragraph.

## Measurement / motivation section

A measurement paper *is* the measurement section, organized
phenomenon-by-phenomenon; each subsection runs its own loop: define the
metric → show the surprising number → drill into raw traces/packet captures
→ name the root-cause mechanism ("Upon closer inspection of the traces, we
noticed… By inspecting packet traces… we found that X is responsible").
System papers keep motivation short, citation-heavy, argumentative.

## Design

Open with a roadmap sentence naming the subsection order ("We first show…
Then, we derive… We show that…"). PHY/math derivations sit inline with
numbered equations; only extra derivation detail goes to an appendix.
Subsections map 1:1 to the challenges listed in the intro.

## Evaluation

- **The two-tier "Micro Benchmarks" / "End-to-end Results" split with ■
  run-in items is a wireless idiom, not a networking-wide law.** It holds in
  mmReliable; the wired-core control (PRED, NSDI'25) does not use it. PRED
  splits evaluation by *evidence source*, not by scope: 6.1 Methodology →
  6.2 Testbed Experiments → 6.3 Simulation, with ordinary numbered
  subsubsections (6.3.2, 6.3.4) and paired bold run-ins `Setup:` /
  `Results:` inside each experiment. MobiCom likewise uses numbered
  subsubsections. Pick the split your evidence justifies; do not import ■.
- What survives in both sub-genres: a methodology/setup subsection first,
  named baselines (PRED compares against 9 named schemes), bold run-in
  labels rather than deep nesting, and CDFs for distributions.
- PRED opens §6 with a bulleted list of the questions the evaluation
  answers ("How does PRED perform in practice…? Why does PRED achieve high
  performance?"). That is legitimate here; naming the *subsections* RQ1/RQ2
  is not.
- Testbed description names exact parts: chips, boards, FPGA models,
  frequency, bandwidth, array size, ground-truth rig; commercial devices by
  model name.
- Baselines are named prior systems, plus an **oracle upper bound** where
  one exists. The oracle is a wireless convention (*uncertain elsewhere*):
  PRED has none, it simply lines up 9 named schemes.
- CDF culture is real: reliability/latency distributions as CDFs with the
  median called out in prose.
- Variance: shaded std-dev regions, 2-D std ellipses; the number of runs is
  a specific integer stated in text ("100 experiments", "5 traces of
  30–60 s") — never "several runs".

## Related work and Conclusion

Late (before Discussion/Conclusion). Bold run-in headers per sub-topic, not
chronology — confirmed in the wired core too (PRED's §7 runs "Dynamically
Adjust the RED Threshold.", "Buffer Sizing and AQM in Internet.",
"Congestion Control for Datacenters."). Differentiators: "In contrast to X,
we…"; against the single closest prior work, enumerate the delta "(i)…
(ii)… (iii)…".

**These venues do keep a Conclusion.** PRED closes with a one-paragraph §8
that restates the mechanism, names the state-of-the-art it beat, and folds
future work into the last sentence. Do not drop the section on the theory
that networking papers skip it; they do not.

## Tone

"We" throughout; claims in present tense, procedures in past. Hedging lives
only in Discussion/Future-work and the abstract's final sentence — never
scattered through design/eval. Verbs: demonstrate, observe, confirm,
identify, reveal, achieve.

## Figures and captions

Takeaway captions are a **wireless/measurement habit, not a field-wide
rule**. mmReliable adds a one-line takeaway after the description
("mmReliable has a low probing overhead compared to vanilla 5G NR"); across
PRED's 27 figures not one caption states a finding, they are descriptive
labels (the only additions are reading notes such as "All are normalized to
the results achieved by PRED"). What PRED does instead is tag the evidence
source in the caption itself: "Figure 13:
[Simulation] FCT statistics with different ECN algorithm", "Figure 11:
[Testbed] PRED performance with different …". That tag is worth copying
whenever a paper mixes testbed and simulation results, because it stops a
skimming reviewer from crediting a simulated number to hardware.

Multi-panel figures share one caption with per-panel (a)/(b)/(c) sentences.

## Reviewer expectations

### SIGCOMM's own author guide (first-hand)

Craig Partridge's "How to Increase the Chances Your Paper is Accepted at ACM
SIGCOMM", published as the author guide on sigcomm.org. Quoted directly:

- **Missing detail is the classic systems rejection.** "A number of systems
  papers get rejected because reviewers feel key details of the system are
  missing, details that in most (but not all) cases the authors could have
  provided." The remedy the guide gives is blunt: "Don't leave out a
  critical detail. Find a way to fit it into the paper."
- **Small beats big.** "small systems papers often fare better than large
  systems paper" — a paper "that tackles a modest problem and usually has a
  contribution that can be described in one sentence", versus one juggling
  "three or four important contributions" that it cannot fully describe.
- **Concede your limitations or get rejected for it.** Stating limitations
  "typically strengthens rather than weakens the paper"; if they are not
  conceded, reviewers conclude the authors miss the big picture or did not
  assess their claims objectively, and since the PC "usually does not have
  any way to ensure that the authors will revise their paper", they "will
  typically err on the side of caution and reject".
- **The abstract routes your paper to a reviewer.** It must signal the
  paper's type, because a mis-routed reviewer writes a low-confidence
  review, and "if none of the paper's reviewers are confident of their
  reviews, they are less likely to argue strenuously in favor" at the PC
  meeting.
- **Do not misrepresent prior work.** Reviewers "get annoyed when that
  contribution is exaggerated or, worse, is a reinvention of prior work".
  Buzzwords do not help and sometimes hurt.
- **Measurement papers** must "explain how the data was taken, why the data
  is believable (i.e., what statistical measures were taken to ensure the
  data was sound)". **Modelling papers** die on abstraction ("too many
  papers look for a way to redefine a networking problem into a solvable
  math problem rather than actually solving the networking problem") and on
  i.i.d. traffic models.

Caveat on this source: the guide is undated and its *process* description is
legacy (~250 submissions, "just one accept/reject cycle"). SIGCOMM '26,
NSDI '26, MobiCom '26 and MobiSys '26 all now run rebuttal and/or
one-shot-revision loops. Treat the writing advice as live and the mechanics
as historical.

### MobiCom / MobiSys reviewer culture (first-hand, from the CFPs)

No separate reviewer-facing guideline document is published for either
venue; the CFPs are the authoritative statement of what reviewers are told
to reward. What they say:

- **MobiCom '26 states its bias explicitly**: the review process "will
  favor papers that describe how the authors will provide access to
  codebases, well-documented datasets, modeling and/or simulation tools to
  support the reproducibility of their systems/methods as well as papers
  that highlight and discuss not only the significance but also the
  limitations of the work." A limitations discussion and a reproducibility
  statement are scored items here, not politeness.
- **Novelty is traded against maturity, on the record**: "the more novel
  the concept, the harder it can be to fully develop or evaluate all its
  aspects. On the other hand, the more practical and developed the system,
  the more simple and sometimes known techniques must be leveraged. The
  review process will take both cases into account." Pick one end and own
  it; a paper that is neither novel nor mature loses on both readings.
- **Rebuttals are tightly scoped.** MobiCom: ≤ 500 words, restricted to
  correcting factual errors or answering reviewer questions, and it "must
  not include new experiments, new data, or new figures" nor promise future
  work. MobiSys is looser: also ≤ 500 words, but new experiments *are*
  allowed when they directly address reviewer feedback, and authors may
  promise results due by camera-ready.
- **Acceptance is conditional at both venues.** Anonymous shepherding runs
  4–6 weeks and the shepherd may demand new experimental results, not just
  editorial fixes. MobiCom's one-shot-revision decision comes with at most
  three reviewer-articulated major changes, and those may require new
  experiments.
- **Rejection carries a paper trail.** A MobiCom reject is embargoed for 11
  months, and a resubmission to MobiCom must report the previous reviewers'
  major concerns and how they were addressed; doing the same for a paper
  rejected at MobiSys/SIGCOMM/NSDI/SenSys/UbiComp is "strongly encouraged".
  MobiSys collects the same summary out-of-band and shows it to reviewers
  only after they have submitted their reviews, to avoid bias.
- **MobiSys '26 publishes a one-page public review** of every accepted
  paper, written by a TPC member, on the website and in the proceedings.
  Combined with single-blind review, this is a materially more exposed
  process than SIGCOMM's.

## Reviewer personas at this venue

- **A — domain expert**: knows the measurement literature for this layer.
  Hunts contradictions with prior measurement findings, missing closest
  systems, and whether the claimed regime (frequency band, mobility,
  topology) actually generalizes beyond the testbed.
- **B — methods hawk (testbed realism)**: exact hardware named? run counts
  as integers? variance shown (shaded std, error bars, CDFs with medians
  called out)? oracle upper bound present, where the problem admits one? Is
  the root cause *traced* (packet captures, traces) or merely asserted?
- **C — busy PC member**: does the funnel intro justify the mechanism;
  would the "(i)…(iv)" novelty list survive a skim of the cited priors;
  scope discipline — one mechanism nailed beats a stack redesign.
- **Field must-checks**: an evaluation split that the evidence justifies
  (micro-bench → end-to-end, or testbed → simulation) with a
  methodology/setup subsection first; per-phenomenon observe → drill → name
  loops in measurement sections; a stated limitations discussion, which
  MobiCom's CFP says reviewers favour. Missing system details the authors
  clearly had is the classic SIGCOMM rejection (the author guide says so
  outright) — hunt for them.
- **Do not flag as defects**: a descriptive figure caption with no takeaway
  line, or a testbed/simulation evaluation split instead of
  micro-bench/end-to-end. Both are normal in wired-core networking; the
  takeaway caption and the ■ two-tier split are wireless habits. Do flag a
  caption that hides whether the number came from hardware or simulation.

## Sources

Read 2026-08-06, all primary.

- SIGCOMM '26 and '25 submission instructions —
  conferences.sigcomm.org/sigcomm/2026/submission/ and .../2025/submission/
- NSDI '26 call for papers — usenix.org/conference/nsdi26/call-for-papers
- MobiCom '26 call for papers — sigmobile.org/mobicom/2026/cfp.html
- MobiSys '26 call for papers —
  sigmobile.org/mobisys/2026/call_for_papers/
- INFOCOM '26 submission guidelines (main conference) —
  infocom2026.ieee-infocom.org/submission-guidelines-main-conference
- SIGCOMM author guide, Craig Partridge —
  sigcomm.org/for-authors/hints-tips-and-guides/author-guide (live host was
  unreachable on 2026-08-06; text read from the Wayback Machine capture)
- Wired-core control paper: X. Du et al., "PRED: Performance-oriented Random
  Early Detection for Consistently Stable Performance in Datacenters",
  NSDI '25 — usenix.org/conference/nsdi25/presentation/du
