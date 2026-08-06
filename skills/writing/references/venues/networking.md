# Networking / wireless / mobile venue profile

Venues: SIGCOMM, NSDI, MobiCom, MobiSys, INFOCOM. Grounded in full reads of
mmReliable (SIGCOMM'21), Gemini (MobiCom'24), and an INFOCOM'21 WiGig
measurement study — strongest for the wireless/mmWave sub-genre; re-verify
before applying wholesale to wired-core SIGCOMM papers (*uncertain*).

## Format facts

- SIGCOMM: 2-column 10pt acmart (9pt from 2025), 12 pp body + free
  refs/appendix. NSDI: 12 pp final. Double-blind.
- Figure-heavy culture: 10–16 figures on 10–15 pages; tables only for
  compact numeric grids (device × metric).

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
don't transfer. Figure 1 is a two-panel schematic: "(a) Conventional
[failure] (b) OurSystem [success]". Contribution style splits by sub-venue:
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

- SIGCOMM idiom: two tiers — **"Micro Benchmarks"** then **"End-to-end
  Results"**, with bolded inline run-in items ("■ SNR gain due to …:")
  instead of numbered subsubsections. MobiCom uses numbered subsubsections.
- Testbed description names exact parts: chips, boards, FPGA models,
  frequency, bandwidth, array size, ground-truth rig; commercial devices by
  model name.
- Baselines are named prior systems plus an **oracle upper bound**.
- CDF culture is real: reliability/latency distributions as CDFs with the
  median called out in prose.
- Variance: shaded std-dev regions, 2-D std ellipses; the number of runs is
  a specific integer stated in text ("100 experiments", "5 traces of
  30–60 s") — never "several runs".

## Related work

Late (before Discussion/Conclusion). Bold run-in headers per sub-topic, not
chronology. Differentiators: "In contrast to X, we…"; against the single
closest prior work, enumerate the delta "(i)… (ii)… (iii)…".

## Tone

"We" throughout; claims in present tense, procedures in past. Hedging lives
only in Discussion/Future-work and the abstract's final sentence — never
scattered through design/eval. Verbs: demonstrate, observe, confirm,
identify, reveal, achieve.

## Figures and captions

Unlike systems venues, captions here often add a one-line takeaway after
the description ("mmReliable has a low probing overhead compared to vanilla
5G NR"). Multi-panel figures share one caption with per-panel (a)/(b)/(c)
sentences.

## Reviewer expectations

SIGCOMM's author guide (secondhand, *uncertain*): rejections commonly cite
missing system details the authors clearly had; small papers that nail a
modest problem beat large papers juggling many goals. Both papers read
scope tightly to one mechanism — match that.
