# Journal venue profile

Two regimes that bracket conference culture: Nature/Science short-form
(inverted narrative) and IEEE/ACM Transactions (strict IMRaD, extended
conference papers). Grounded in full reads of the Nature chip-placement
paper (2021), AlphaZero (Science 2018, author preprint — layout facts
*uncertain*), and two IEEE/ACM ToN papers, plus ToN's official submission
rules and Nature's official summary-paragraph template.

## Nature / Science

### Structure is inverted — conclusions first, methods last

- No "Introduction" heading: the body opens in medias res with narrative.
- Order: abstract → untitled narrative intro → Results with run-in
  headings → short Conclusion → **References → Methods** (after the
  references!) → Data/Code availability → Extended Data.
- Related work is folded *inside Methods*, nearly the last narrative text
  in the paper. Science goes further: Methods is demoted to a single
  reference ("(10) See the supplementary materials") and lives entirely in
  the Supplement.

### Abstract — Nature's official 6-move template (primary source)

1. Basic introduction any scientist can follow (1–2 sentences).
2. Detailed background for the field (2–3).
3. The specific problem (1).
4. Main result, opened with **"Here we show"** or equivalent (1).
5. Contrast with what was previously believed (2–3).
6. Optional broader context (2–3; with it, cap ~300 words).

The 2021 chip paper matches move-for-move at 202 words; Science abstracts
run shorter (~120 words), same skeleton without the literal "Here we show".

### Hard limits

Main text ~3,500–4,300 words; **≤6 display items**; figure legends <250
words; abstract without citations (*limits cross-checked against the
published paper but the official guide sits behind a login — uncertain*).
Citations: Nature superscript numbers; Science parenthesized "(1, 2)",
"(16–18)" — a mechanical rewrite when switching between them.

### Tone

First-person active, past tense for what was done, but *narrative* — a
story with one arc, not a contribution list. Every detail that doesn't
serve the arc moves to Extended Data / Supplementary.

## IEEE/ACM Transactions (ToN read closely; TPDS/TSE/TOCS unverified)

### Structure

Strict Roman-numeral IMRaD. The Introduction itself carries lettered
subsections: "A. Our Contributions", "B. Novelty and Related Work",
"C. Organization" (a roadmap subsection is expected here, unlike USENIX
conferences). Theory papers put full Theorem/Lemma/Proof chains in the
body — exactly the material a conference version compresses into an
appendix; the page budget exists to unfold it.

### Hard rules (ToN official, primary source)

- Abstract 150–250 words, one paragraph, no equations/tables, no
  citations/abbreviations; 3–4 Index Terms.
- 16 pp two-column 10pt max (beyond needs editor approval). Wrong format
  is returned unreviewed. Single-blind, ≥2 reviewers.
- Double submission = immediate rejection at both venues.

### Conference-to-journal extension

**There is no official "30% new material" rule at ToN** — the requirement
is a cover letter explaining the delta, and no verbatim republication.
The idiomatic in-paper move is a "Novelty and Related Work" subsection that
enumerates the delta explicitly: "In this article, we significantly improve
and generalize [conf]: (a)… (b)… (c)…" and names what the short paper
lacked ("without any technical details, proofs or evaluations").
What to add when extending: full proofs, more experiments, longer related
work — unfolded, not padded.

### Tone

Formulaic "we" with enumerated contributions "(1)… (2)… (3)"; far less
narrative than Nature. Figures skew architectural/diagrammatic rather than
data-photographic.

## Reviewer personas at this venue

- **Nature/Science — editor-gatekeeper first**: the binding filter is
  editorial, not peer review — would a scientist outside the field care?
  Persona A plays the editor (broad significance, narrative arc, "Here we
  show" clarity); B plays the field referee (are Methods, buried at the
  end, actually sufficient to reproduce); C checks display-item discipline
  (≤6, legends self-contained) and whether claims in the main text lean on
  Supplementary material a reader never sees.
- **Transactions — completeness referees**: single-blind, ≥2 reviewers,
  no rebuttal theatre. A: is the delta over the conference version explicit
  and real (proofs unfolded, new experiments), not restatement; B: do the
  theorem chains hold and are all claimed cases covered; C: IMRaD
  discipline, abstract within 150–250 words, Index Terms present.
- **Field must-checks**: for extensions, demand the self-stated delta
  paragraph ("In this article we improve [conf] in several ways: (a)…").
  Do **not** demand a fixed percentage of new material — no such official
  rule at ToN; judge the delta on substance.
