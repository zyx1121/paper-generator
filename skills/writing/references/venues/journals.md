# Journal venue profile

> Facts verified: 2026-08-06 — format rules (pages, templates, checklists,
> deadlines-adjacent mechanics) decay yearly; re-verify against the live CFP
> before relying on them.

Two regimes that bracket conference culture: Nature/Science short-form
(inverted narrative) and IEEE/ACM Transactions (strict IMRaD, extended
conference papers). Grounded in full reads of the Nature chip-placement
paper (2021), AlphaZero (Science 2018), two IEEE/ACM ToN papers and one
TPDS paper, plus the official author instructions of Nature, Science, ToN,
TPDS, TSE, ACM TOCS and the IEEE Computer Society.

Sources for the format facts below (all fetched or re-fetched 2026-08-06):
Nature formatting guide (login-walled live; read via a `web.archive.org`
snapshot); Science "Information for Authors" and "Preparing your initial
manuscript" (live site 403s any non-browser client; read via
`web.archive.org` snapshots of the Aug-2025 captures); `computer.org`
"How to Get Published" author guidelines and the per-journal Author
Information pages for TPDS and TSE; ACM DL TOCS author guidelines (live
403; `web.archive.org` snapshot).

## Nature / Science

### Structure is inverted — conclusions first, methods last

- No "Introduction" heading: the body opens in medias res with narrative.
- Nature's official assembly order: title → authors → affiliations → **bold
  first paragraph** (the summary paragraph) → main text → main references →
  tables → figure legends → **Methods** (including data and code
  availability statements) → methods references → acknowledgements → author
  contributions → competing interests → additional information → Extended
  Data legends. Methods really does sit after the reference list.
- Related work is folded *inside Methods*, nearly the last narrative text
  in the paper. Science goes further: Materials and Methods live entirely
  in the supplementary materials and are reached from the main text by a
  numbered citation.

### Abstract — Nature's official 6-move template (primary source)

1. Basic introduction any scientist can follow (1–2 sentences).
2. Detailed background for the field (2–3).
3. The specific problem (1).
4. Main result, opened with **"Here we show"** or equivalent (1).
5. Contrast with what was previously believed (2–3).
6. Broader context (2–3 sentences putting the findings in general context).

Nature's formatting guide caps this summary paragraph at **ideally ≤200
words**, fully referenced, separate from the main text, aimed at readers
outside the discipline, avoiding numbers, abbreviations, acronyms and
measurements unless essential. The 2021 chip paper matches move-for-move at
202 words.

Science's abstract rules are different and stricter: **≤125 words**, one
paragraph, no citations, no abbreviations, structured BACKGROUND →
OBJECTIVES/METHODS → RESULTS → CONCLUSIONS. The "Here we show" phrasing is
a Nature convention, not a Science one.

### Hard limits — Nature (primary source)

- Length is budgeted in *print pages*, not words: a typical 6-page Article
  is **~2,500 words with 4 modest display items**; a typical 8-page Article
  is **~4,300 words with 5–6 modest display items**. A "modest" display
  item plus legend occupies about a quarter page (~270 words of budget); a
  half-page composite figure costs ~600 words. Text shrinks to pay for
  figures.
- Figure legends **<300 words each**, no methods detail inside them.
- **≤50 references** in the main text as a guideline; Methods and
  Supplementary references are not counted.
- Methods typically **≤3,000 words**, and may contain no figures or tables
  (those go to Extended Data). Typically **≤10 Extended Data display
  items**.
- Citations are superscript numbers.

### Hard limits — Science (primary source)

- Research Article, standard format: **main text ≤3,000 words**, plus
  abstract, **3–5 display items** with brief legends, **~50 main-text
  references** and a structured acknowledgments section. Main text is
  divided into sections with brief descriptive subheadings (up to three
  levels).
- Research Article, **extended online format** (chosen at submission): main
  text up to **6,000 words**, up to **6 display items**, up to **100
  main-text references**; the cover letter must argue why the extra length
  is merited.
- Materials and Methods go to the supplementary materials, along with any
  additional data and figures needed to support the conclusions.
- Title ≤96 characters including spaces; short title ≤40 characters; figure
  captions ≤200 words.
- Citations are italic numbers in parentheses: "(18, 19)", "(18–20)",
  "(18, 20–22)" — a mechanical rewrite when switching from Nature's
  superscripts. One combined reference list covers main text and
  supplement.
- Assembly order (the submission system extracts metadata from these exact
  headings): Title → Authors → Affiliations → Abstract → Main Text →
  References and Notes → Acknowledgements → List of Supplementary
  Materials → Fig. # → Table #. Acknowledgements carry Funding, Author
  contributions, Competing interests, and Data and materials availability.
- Two things a preprint's layout can mislead you about. **There is no
  one-sentence summary field** for a Science Research Article — the
  assembly order has none, and a one-sentence abstract is required only for
  Perspectives and Policy Forums (any "≤125/135-character one-sentence
  summary" you have seen belongs to sibling AAAS journals, not Science).
  And **"Report" is no longer a Science format** — the current instructions
  list Research Articles only, split into standard and extended online.

### Tone

First-person active, past tense for what was done, but *narrative* — a
story with one arc, not a contribution list. Every detail that doesn't
serve the arc moves to Extended Data / Supplementary.

## IEEE/ACM Transactions

### Structure

Numbered IMRaD. The Introduction itself carries lettered subsections in the
ToN papers read here: "A. Our Contributions", "B. Novelty and Related
Work", "C. Organization" (a roadmap subsection is expected, unlike USENIX
conferences). Theory papers put full Theorem/Lemma/Proof chains in the
body — exactly the material a conference version compresses into an
appendix; the page budget exists to unfold it.

Two structural variants worth not over-generalizing (from a full read of a
TPDS paper, author copy):

- **Section numbering is not uniformly Roman.** The ToN papers use Roman
  numerals; the TPDS paper numbers sections in Arabic (1, 2, …). Follow the
  journal's own template rather than a remembered house style.
- **Related work is not always an Introduction subsection.** The TPDS paper
  places Related Work as the penultimate section, right before Conclusions,
  with the Introduction ending in an explicit roadmap sentence
  ("… Section 8 describes related works and Section 9 concludes this
  paper."). Both placements are idiomatic; pick one and be consistent.

Every IEEE Transactions paper also ends with an author biography (and, for
full-length journal articles, author photos) — and that biography counts
against the page limit.

### Hard rules — IEEE/ACM ToN (official, primary source)

- Abstract 150–250 words, one paragraph, no equations/tables, no
  citations/abbreviations; 3–4 Index Terms.
- 16 pp two-column 10pt max (beyond needs editor approval). Wrong format
  is returned unreviewed. Single-blind, ≥2 reviewers.
- Double submission = immediate rejection at both venues.

### Hard rules — IEEE Computer Society journals (TPDS, TSE and siblings)

Shared across every IEEE CS journal (official author guidelines):

- **Abstract 100–200 words** for a regular or special-issue paper (50 words
  for a short paper), no mathematical expressions, no bibliographic
  references. Note this is a *narrower* window than ToN's 150–250.
- **A double-column page is defined as 7.875″ × 10.75″ with 9.5-point type
  and 11.5-point vertical spacing** — that definition is what the page
  counts below are measured in. Using the journal template is mandatory for
  journal submissions.
- **Mandatory Overlength Page Charges (MOPC)**: the regular-paper limit is
  **12 formatted pages** for Transactions (4 for Letters), **including
  references and author biographies**; every page or fraction beyond it is
  charged **$220**, assessed after final editing and layout, invoiced at
  galley-proof approval. Enforcement has teeth: unpaid mandatory charges
  bar the authors from submitting to IEEE publications until settled.
  Submission page limits and MOPC thresholds are *different numbers* — see
  per-journal rules below.
- **Appendices are supplemental material**, submitted as separate files
  (never inside the main PDF); if an appendix is left in the main file it
  is sent back. Supplemental files have no page limit.
- In-text citations are square-bracketed for journals (superscript is the
  magazine style).
- Review model: **single-anonymous by default** (authors named to
  reviewers), **≥3 independent reviewers** solicited, EIC decides, and a
  prescreen can reject before review. Roughly 25% of submissions are
  accepted. Double-anonymous review is available *on request with written
  justification, at the EIC's discretion* — but **TSE, TC, TCC, TDSC and
  TETC do not offer it at all**.
- Submission mechanics: ScholarOne / IEEE Author Portal; **an ORCID is
  required by all IEEE publications** and is prompted for at account
  creation and again at submission; ≥3 keywords chosen from the ACM
  taxonomy in the submission form, because the system matches those
  keywords to reviewers. The pre-submission checkers on the journal side
  are the **IEEE LaTeX Analyzer**, the **IEEE Template Selector** and the
  **IEEE Reference Preparation Assistant** — PDF eXpress is a conference
  tool and plays no part in the journal flow.
- Concurrent submission to another publication or conference during review
  is an automatic rejection at IEEE, with possible publication sanctions.

**TPDS specifics** (official Author Information):

- Regular paper **12 double-column pages**; **submissions may run up to 18
  pages**, with everything past 12 charged at the MOPC rate after layout.
- Comments paper 2 pages; **survey paper 14 pages**.

**TSE specifics** (official Author Information):

- **No strict submission page limit**, but the manuscript is expected to be
  **under 16 pages**, and the editorial board may ask for fewer if a paper
  reads as unnecessarily long. Past **12 double-column pages after final
  layout**, MOPC applies.
- Acceptance criteria are stated as three tests: a substantial novel
  contribution, convincing evidence (analytical, empirical or
  experiential), and clear accurate presentation. A significant weakness on
  any one of them earns an **administrative rejection before full review**.
- "Revise and resubmit as new" is a real outcome: the resubmission is
  treated as a new submission, though authors may request reviewer
  continuity.
- TSE splits the manuscript type by provenance: **Regular (Journal First)**
  for wholly new results (requires a 200-word novelty statement; accepted
  journal-first papers may be invited to present at ICSE) versus
  **Regular (Extension)** for conference extensions.

**ACM TOCS specifics** (official author guidelines):

- Submission through ACM Manuscript Central as PDF, with a **cover letter
  arguing scope fit**. The ACM authoring template is required for both
  submission and publication. ORCIDs are required for all authors before
  publication.
- The guidelines state **no page limit and no abstract word limit** — the
  binding constraint is the ACM template, which approximates final page
  count. The one length figure given is for the Research Highlights type
  (below).
- **Research Highlights** is a TOCS-specific paper type: a shorter, more
  readable version of a published conference paper for a broader audience,
  target **~5,000 words counting each figure or table as ~250 words** (not
  strictly enforced).
- The author-guidelines page does not state a blinding model; it defers to
  the ACM Peer Review Policy.

### Conference-to-journal extension — the rule is venue-specific

This is where the four venues genuinely disagree. Do not carry one venue's
rule to another.

| Venue | Official requirement |
| --- | --- |
| **ACM (TOCS, and the ACM Journals norm)** | **At least 25% new content** — an actual stated percentage. Plus a first-page footnote listing the authors' relevant prior publications and stating this manuscript's contributions beyond them. Research Highlights must still meet 25–30% new material. |
| **TPDS** | **No percentage, deliberately** — "the specific amount of acceptable new content is subjective and depends on the reviewer". |
| **TSE** | A dedicated **"Regular (Extension)"** manuscript type with an explicitly *low* novelty bar. |
| **IEEE/ACM ToN** | No percentage rule; a cover letter explaining the delta, and no verbatim republication. |
| **IEEE CS generally** | Cite the prior work, state how the submission is substantively novel, attach copies of the prior papers, and give a brief description of the differences. Editors and reviewers judge "whether a sufficient amount of new material has been added". |

TPDS is the most explicit about *what counts*, and its taxonomy is the best
checklist to write against:

- **Acceptable**: new conceptual extensions; experiments that provide new
  insights; new theoretical analysis and/or proofs supporting empirical
  results.
- **Allowable but insufficient on its own**: more background or related
  work; elaboration on the same points in the introduction, observations
  and conclusions; extra figures that merely illustrate already-published
  content; **additional experimental results without new insights**.
- **Unacceptable**: a simple union of content from multiple prior
  publications.

TPDS also requires the submission to answer three questions explicitly:
what are the novel contributions beyond the previous publication(s); what
is the new content and in which sections does it appear; how do those
contributions build on the previously published material. Answering these
three in a "Novelty and Related Work" subsection is the idiomatic in-paper
move: "In this article, we significantly improve and generalize [conf]:
(a)… (b)… (c)…", naming what the short paper lacked ("without any technical
details, proofs or evaluations").

TSE is the outlier in the permissive direction: its Regular (Extension)
type explicitly accepts "additional proofs or algorithms or other such
details presented for completeness, or additional empirical results, or
minor enhancements or variants" — the exact material TPDS calls
insufficient. TSE asks for a statement explaining the extensions and
encourages a change-marked PDF. Extensions of journal papers, or of
conferences whose proceedings appear in a journal (e.g. FSE via PACM), are
not accepted as extensions at TSE.

### Tone

Formulaic "we" with enumerated contributions "(1)… (2)… (3)"; far less
narrative than Nature. Figures skew architectural/diagrammatic rather than
data-photographic.

## Reviewer personas at this venue

- **Nature/Science — editor-gatekeeper first**: the binding filter is
  editorial, not peer review — would a scientist outside the field care?
  Persona A plays the editor (broad significance, narrative arc, "Here we
  show" clarity); B plays the field referee (are Methods, buried at the end
  or in the supplement, actually sufficient to reproduce); C checks the
  page budget arithmetic (display items against the 6-page/8-page Nature
  budget or Science's 3–5, legends self-contained and inside 300/200
  words) and whether claims in the main text lean on Supplementary material
  a reader never sees.
- **Transactions — completeness referees**: single-anonymous, ≥3 reviewers
  at IEEE CS journals, no rebuttal theatre, and a prescreen that can reject
  on format or scope before anyone reviews the science. A: is the delta
  over the conference version explicit and real (proofs unfolded, new
  experiments *with new insights*), not restatement; B: do the theorem
  chains hold and are all claimed cases covered; C: IMRaD discipline,
  abstract inside the venue's window (100–200 words IEEE CS, 150–250 ToN),
  Index Terms present, page count inside the submission cap with references
  and biographies counted.
- **Field must-checks**: for extensions, demand the self-stated delta
  paragraph and, at TPDS, answers to its three questions. Check the
  *venue's own* rule on how much is enough before demanding a percentage:
  ACM does state 25%, TPDS deliberately refuses to state one, and TSE
  accepts extensions that add only proofs or extra empirical results.
