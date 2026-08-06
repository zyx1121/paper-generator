# Systems / cloud infrastructure venue profile

> Facts verified: 2026-08-06 (re-verified) — format facts read first-hand from
> the OSDI '26, USENIX ATC '25, EuroSys '26, ICDCS '26 and Middleware '26 CFPs.
> Format rules (pages, templates, checklists, deadlines-adjacent mechanics)
> decay yearly; re-verify against the live CFP before relying on them.

Venues: OSDI, SOSP, ATC, EuroSys (USENIX/ACM tier); ICDCS, IC2E, Middleware
(IEEE/ACM second tier). Grounded in full reads of ServerlessLLM (OSDI'24),
vLLM (SOSP'23), Tangram (ICDCS'24); structural reads (section tree,
introduction, related work, captions, number style) of the author preprints of
DistServe (OSDI'24), Llumnix (OSDI'24), TrimCaching (ICDCS'24) and B-Side
(Middleware'24); a title census of six 2024 programs (~90 titles); and the
venues' own CFPs. Preprint text can drift from the camera-ready, so the
headline numbers quoted below come from the published abstracts.
Second-tier evidence is now n=3, and it splits far more than the earlier n=1
read suggested — see below for which tier claims survived.

## Format facts

- **OSDI '26**: 12 single-spaced pages "including figures and tables, plus as
  many pages as needed for references"; accepted papers get 14 pp + references.
  The anti-padding rule is the CFP's own: "Papers should be the right length,
  which may be less than 12 single-spaced pages. Reviewers will be encouraged
  to down-rank overly padded papers. However, papers of 6 pages or less are
  unlikely to receive full consideration." Off-format submissions are
  "desk-rejected without review"; so are anonymization violations. This
  padding language is **new in OSDI '26** — OSDI '25 warned only against
  papers "so short as to be considered 'extended abstracts'". Do not attribute
  it to the USENIX tier generally without checking that venue's CFP.
- **Appendix accounting differs across the USENIX tier** — check the year's
  CFP, never assume. ATC '25 excludes references *and* appendices from its
  12 pp (6 pp for short papers). EuroSys '26 counts appendices inside the
  12 pp and excludes only references. OSDI takes optional supplementary
  material as separate files that PC members are not required to read, so the
  submission must stand alone without it.
- **ICDCS '26**: IEEE 8.5×11 two-column 10pt template, **11 pp including
  figures, tables, appendices and references**; "Papers exceeding this page
  limit or with smaller fonts will be desk-rejected without review."
- **Middleware '26**: ACM sigconf, font size **9pt**, at most 12 pp of
  technical content (text, figures, appendices) excluding references;
  decisions are accept / minor revision (one-shot) / major revision
  (resubmit next cycle) / reject. Double-blind throughout both tiers.

## The two tiers write differently

Re-checked at 4 USENIX-tier and 3 second-tier papers. Two of the three
differences reported from the original n=1 read did not survive. What is left
is narrower — and still a default, not a law.

**Holds.**

1. **Roadmap paragraph.** Both ICDCS papers end the introduction with "The
   remainder / rest of this paper is organized as follows…" (Tangram,
   TrimCaching). Neither OSDI paper has one, and neither does the Middleware
   paper. Write one for ICDCS; omit it at the USENIX tier.
2. **Precision of reported percentages.** The ICDCS papers quote two-decimal
   percentages throughout (Tangram: 13 distinct values, e.g. 74.30%;
   TrimCaching: 7). The two OSDI papers use *none* — every percentage they
   report is one-decimal or integer, and the headline result is a multiplier
   (7.4×, 12.6×, 1.5×). Middleware sits between (B-Side: one two-decimal
   value, otherwise integers). The discriminator is percentage precision;
   multiplier precision is not a tier signal (the DistServe preprint headlines
   4.48× where the published version says 7.4×).

**Refuted — do not apply.**

3. *"IEEE tier inserts a dedicated Motivation/Challenge section; USENIX folds
   motivation into the first two sections."* Llumnix (OSDI'24) has a
   standalone §3 "Motivation"; DistServe's §2 is "Background and Motivation",
   followed by a whole §3 "Tradeoff Analysis"; B-Side's §2 is "Background and
   Challenges". A separate motivation/challenge section before Design is
   normal at **both** tiers — and TrimCaching (ICDCS) has none at all.
4. *"IEEE tier states contributions in narrative prose."* Four of the five
   introductions checked use a contribution list: DistServe 3 bullets,
   Llumnix 4 bullets, TrimCaching 4 enumerated items, B-Side 2 numbered items.
   Tangram's prose contributions are the outlier, not the tier's rule.

## Title

`SystemName: Claim` is the default (EuroSys'24: 14/14; OSDI'24: 10/15).
Inverted variant: claim first, "with SystemName". Do not hard-code the
colon: vLLM's title has no colon and no system name — the algorithm name
carries it. IC2E tolerates question titles; OSDI/SOSP/EuroSys don't use them.

## Abstract

4–8 sentences, 120–160 words. Two openings, both legitimate:
problem-first (context → problem → solution → result) or system-first
("This paper presents X, a … that …"). One or two headline numbers — a
multiplier at the USENIX tier (DistServe, published abstract: "can serve 7.4×
more requests or 12.6× tighter SLO"), a two-decimal percentage at ICDCS.
Optional last sentence: artifact link.
Do not thread more than ~3 numbers through the abstract — density of inline
percentages reads as foreign at these venues.

## Introduction

4–9 paragraphs (DistServe 9, B-Side 6, Tangram 4): domain stakes → technical
bottleneck → problem quantified (cite Figure 1) → key observation ("We observe
that …") → system + headline number → contributions. Figure 1 is an overview
or a motivating measurement; its caption is a descriptive label, not a claim
sentence.

Contributions are a list of 2–4 items at both tiers. Two phrasings, both
attested: "We identify / We propose / We design and implement / We evaluate"
(Llumnix, B-Side) or bare verb-first items with the "We" dropped ("Identify
… / Design … / Conduct …", DistServe). A §-ref per bullet is optional, not
expected — none of DistServe, Llumnix or B-Side carries one (*the earlier
"each with a §-ref" rule was over-stated*). Add an ICDCS-style roadmap
paragraph after the list only for the second tier.

## Design

- Open by pointing back at the problem section in one sentence, then either
  an architecture figure walk (vLLM) or a named list of design concerns that
  map 1:1 onto the following sections (ServerlessLLM).
- IEEE-tier papers may add a formal problem/optimization statement — accepted
  there (TrimCaching devotes three sections to formulation, mapping and
  approximation guarantees), out of place at the USENIX tier.
- Present tense; subject is the system name or "we". State design claims
  flatly; reserve hedging for empirical observations.

## Evaluation — NOT organized by RQs

None of the seven papers read uses RQ1/RQ2 headers (that is SE dialect) —
the single most robust finding in this profile. The canonical shape:

1. **Experimental Setup / Setting first** — testbed, versions, workloads,
   named baselines and tuning, metrics, runs/variance. True in 4 of 5 papers
   re-checked; B-Side (Middleware'24) is the exception, opening evaluation
   with Validation instead.
2. **Per-component / per-workload subsections** — named after the component
   ("X Checkpoint Loading", "Migration Efficiency") or the workload
   ("Chatbot", "Shared prefix"). Order relative to end-to-end varies:
   DistServe runs end-to-end immediately after setup, then drills down.
3. **End-to-end / integration** — community idiom for the title: "Entire X
   in Action", "Deep Dive into X".
4. **Ablation** — its own subsection or top-level section where the design has
   separable parts, but it is not universal: DistServe has one, Llumnix and
   Tangram do not. IEEE tier may add a dedicated **Accuracy** subsection.

Baselines are named systems (never just "baseline"); include an oracle
upper bound where one exists. Narrate claim-first: state "X sustains
1.7–2.7× higher rates than Orca" before walking the figure. Line charts for
latency-vs-load, bars for memory/cost, CDFs in deep-dive subsections.

## Related work

**USENIX tier: late** — after Evaluation, before Conclusion (DistServe §7,
Llumnix §7, ServerlessLLM, vLLM). Flat thematic paragraphs opened by a bolded
run-in topic phrase ("Inference serving.", "Resource disaggregation.").

**Second tier: check the venue, it splits.** Of three papers, only Tangram
places related work late; TrimCaching puts it at §2 and B-Side at §3, both
immediately after the introduction. Sub-sectioning splits too — Tangram uses
numbered subsections, TrimCaching one flat section, B-Side bolded run-in
heads like the USENIX tier. Match the recent papers of the specific venue
rather than the tier (*the earlier "IEEE tier: named subsections" rule rested
on Tangram alone and does not generalize*).

Highest citation density of any section: 18–30 refs in related work, out of
43–90 total. ICDCS/Middleware papers sit at the low end (43–56 total) because
the 11–12 pp limit includes or crowds the bibliography. Every cluster ends
with a differentiator — "However/Unlike [prior], [System] …", or a
relationship statement ("DistServe is orthogonal to …", "DistServe adopts a
similar concept but …"). Name the single closest system and state the
relationship explicitly (complementary vs. superseding).

## Figures, tables, citations

7–19 figures and 1–5 tables (DistServe 12F/2T, Llumnix 16F/1T, Tangram
14F/4T, B-Side 9F/5T, TrimCaching 7F/1T). Figure counts scale with the page
limit, so 11 pp second-tier papers run leaner. The USENIX tier is **not**
table-free — specs can live in prose, but both OSDI papers still carry
workload/configuration tables; the IEEE tier leans harder on results tables.

Captions are descriptive labels — the "caption states the finding" advice is
not how these venues write (*0 of 7 papers read use claim-captions; verified
across ServerlessLLM, vLLM, Tangram, DistServe, Llumnix, TrimCaching,
B-Side*). A caption may be a full sentence, but it describes what the figure
shows, not the paper's headline result.

## Reviewer expectations

Middleware's published criteria, verbatim from its CFP: "the significance of
the problem, the novelty of the solution, advancement beyond prior work,
sufficient supporting evidence, and clarity of the presentation." OSDI's
parallel list: motivate a significant problem, propose a compelling solution,
demonstrate practicality and benefits, draw appropriate conclusions, clearly
describe the contributions, clearly articulate the advances beyond previous
work. Classic kills: missing closest-system baseline, evaluation that dodges
the paper's own claims, padding. Desk rejects: page/format violations (OSDI
and ICDCS both say "without review"), broken anonymization.

## Reviewer personas at this venue

- **A — domain expert**: lives in the serving/serverless/checkpoint
  literature. Hunts the uncited closest *system* (the classic systems kill:
  "you didn't compare against X"), overlap with named prior systems, and
  whether the stated delta survives a read of those systems' papers.
- **B — methods hawk (SIGPLAN empirical)**: baselines fairly tuned, run
  counts and variance, tails not just means, workload cherry-picking,
  ablations attributing the gain — and padding, which OSDI '26 makes an
  explicit reviewer instruction ("Reviewers will be encouraged to down-rank
  overly padded papers").
- **C — busy PC member**: 15 papers in the stack. Does the contribution
  list survive the details; is Figure 1 comprehensible alone; does the
  design section give rationale for each contestable choice.
- **Field must-checks**: evaluation opens with setup and is organized by
  component/workload, not RQ headers (RQ headers read as SE dialect — flag);
  related work late at the USENIX tier, venue-matched at the second tier;
  claim-first narration backed by the cited figure. Do **not** demand a
  Threats-to-Validity section or RQ headers — wrong field.
