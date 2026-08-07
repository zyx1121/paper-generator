# Academic prose style reference

Distilled from Simon Peyton Jones, Michael Ernst, Norman Ramsey ("Two Hours
per Week"), Gopen & Swan ("The Science of Scientific Writing"), Jennifer
Widom, Henning Schulzrinne, Williams, and Pinker. Apply these rules while
drafting, and again as a checklist while revising.

## Sentences

- **Active voice, whiteboard language.** "We ran 34 tests", not "34 tests
  were run". "The ball moved sideways", not "the object under study was
  displaced horizontally" (SPJ). Passive only when the agent is genuinely
  irrelevant or to keep old information in subject position.
- **"We" only for what the authors did.** The system is the actor for what
  the system does: "The analysis computes a graph", not "We compute a graph"
  (Ernst). Never anthropomorphize ("the program thinks").
- **Tense:** present for the paper and timeless facts ("Section 5 shows",
  "the algorithm runs in O(n log n)"); past for experiments performed
  ("we measured throughput"). Never future for technical facts.
- **Subject and verb adjacent, action in the verb** (Gopen & Swan). Anything
  wedged between subject and verb reads as an aside and gets lost.
- **Kill nominalizations:** "make an assumption" → "assume"; "perform an
  evaluation of" → "evaluate"; "is a function of" → "depends on".
- **Old-to-new flow (the given-new contract).** Open each sentence with
  something the reader already has (topic position); put the new, important
  material at the end (stress position). Test: read only the sentence
  openings of a paragraph — each should link back to the previous sentence.
- **Emphasis lands at the end of the sentence** (Ramsey, Strunk & White).
- **Singular over plural** (Ramsey): "Each lexical analyzer translates a
  regular expression into an automaton" — plurals hide whether the
  relationship is one-to-one or n-to-m.
- Vary sentence length: short sentences state points; longer ones elaborate.
- No contractions; no sentence-initial "And"; positive form ("forgot", not
  "did not remember").

## Paragraphs

- **Point first.** The first sentence states the paragraph's point; a reader
  skimming only first sentences should reconstruct the whole argument
  (Ramsey, Dreyer). One paragraph, one point — two points means split.
- Paragraph-initial transitions encode the logical relation ("However, this
  bound is loose in practice."), not generic glue.
- **No garden paths** (Ernst): never present an approach and only later
  reveal it fails — warn up front ("A naive approach — which fails, as we
  show — is to …").
- No walls of text (>12 lines in two-column = probably two points), and no
  strings of one-sentence paragraphs.

## Words

- **Consistent terminology — the cardinal CS rule** (Ramsey #1). One term per
  concept, everywhere; "stack frame" and "activation record" in one paper is
  a bug. Unlearn synonym rotation. Name concepts by what they do, never
  "approach 1"/"our approach".
- Define every term and symbol before first use (Widom). Acronyms: expand
  once — "control-flow graph (CFG)" — then acronym only; don't introduce one
  used fewer than 3 times.
- **Banned:** clearly, obviously, easily, trivially, of course · very,
  really, extremely, quite · novel, innovative (the contribution list
  establishes novelty, not adjectives) · significant (unless statistical,
  with the test) · utilize (→use) · in order to (→to) · due to the fact
  that (→because) · etc. after e.g. · thing, stuff, a lot of · "for various
  reasons" (give the reasons) · non-referential "this/that/it" — always
  attach a noun ("this technique").
- **Also banned, and now corpus-measurable** (see the LLM-tells section for
  the evidence): delve into (→examine) · showcase (→show) · underscore
  (→show, or drop the verb and state the fact) · enhance (→improve, with
  the number) · garner (→receive) · intricate (→complex, or say how) ·
  meticulous · commendable · realm · landscape (as metaphor). A second set
  — crucial, comprehensive, insights, notably, particularly, additionally,
  potential, robust — is **rate-limited, not banned**: each is a legitimate
  academic word, and the marker is density, not presence.
- "previous work" not "existing work"; "related work" never "related works";
  "that" for defining clauses, "which"+comma for non-defining; "whether" not
  "if" for alternatives.
- Numbers: only justified digits; "5 percentage points" vs "20% greater" —
  never ambiguous; "half as many", never "2× fewer"; spell out integers
  under ten in prose; no symbols in prose ("for all nodes", not "∀ nodes").
- Hyphenate compound modifiers ("real-time system", "end-to-end latency"),
  but not after -ly adverbs.

## Non-native pitfalls (double-check these)

- Articles: concepts and protocol names take none ("TCP delivers packets";
  "Caching improves performance"); specific instances do ("the router we
  consider"); organizations do ("the IETF").
- "allows to" is ungrammatical → "allows the user to X" / "allows X-ing" /
  "makes it possible to X".
- No "informations", "feedbacks", "researches", "softwares"; "code" is
  uncountable.
- "i.e.," = that is (exhaustive); "e.g.," = for example (non-exhaustive);
  both take the trailing comma. Comma after "However,"/"Therefore,".

## Claims calibration

- **The verb is the claim.** Ladder: conjecture < may indicate < suggests <
  we observe < indicates < shows/demonstrates < establishes < proves
  (theorems only). Microbenchmarks *suggest*; controlled experiments with
  statistics *show*. Reviewers check verb–evidence alignment.
- **Quantify instead of qualify.** "much faster" → "3.2× faster on PARSEC";
  "scales well" → "scales linearly to 64 cores"; "low overhead" → "adds 2.1%
  mean latency". A number is refutable; an adjective is not.
- Scope every claim ("on these workloads", "for programs without
  reflection"). One calibrated hedge per claim, never stacked hedges.
- State limitations yourself; venues instruct reviewers to reward that.

## Math and notation

- Displayed equations are part of the sentence: punctuate them (comma if the
  sentence continues, period if it ends).
- Never start a sentence with a symbol ("The function $f$ is continuous").
- Capitalize as proper nouns: Section 4, Figure 7, Theorem 2, Equation (3);
  lowercase generic uses ("the previous section").
- One symbol per concept, one concept per symbol; define at first use.

## Reads-as-LLM tells — actively counter-program these

> Tells verified: 2026-08-07 — lexical markers re-checked against the
> 2025–2026 corpus literature listed under Sources at the end of this
> section.

**This list has a half-life; read it the way the venue profiles ask you to
read hard format facts** — a dated snapshot, not a rule. Every marker here
is a statistical artifact of one model generation and of one moment in
author behavior, and naming a marker publicly is what kills it: "delve"
dropped sharply in arXiv abstracts within months of being called out in
early 2024, while "significant", equally favored, kept climbing (Geng &
Trotta 2025). Two consequences. First, re-verify against fresh corpus work
when the model generation turns over; a list older than about a year is a
lead, not a lint rule. Second, **absence of these words is not evidence of
human prose** — Geng & Trotta recommend detectors watch for anomalous
*declines* as well as excesses, so mechanical scrubbing produces its own
signature. Rewrite the sentence so the word was never needed.

Because this prose is generated, reviewers and readers will be alert to
these. Treat each as a lint error, but weight them by evidence.

### Corpus-verified — measured frequency shifts in real academic corpora

- **Audit verbs first.** Of the 379 excess style words in 2024 PubMed
  abstracts, 66% were verbs and 14% adjectives, a sharp break from the
  noun-dominated shifts of earlier years (Kobak et al. 2025). The tell
  lives in the verb and modifier layer, not in the technical nouns.
- **Ban outright** — ornamental, with a plain replacement always available:
  delve, showcase, underscore, meticulous, commendable, intricate, garner,
  realm, tapestry, testament, foster, elevate, navigate, vibrant,
  compelling, groundbreaking, seamless, holistic, multifaceted, paramount,
  leverage (→use), "valuable insights", "plays a vital role", "cannot be
  overstated", "marks a significant shift". The highest measured excess
  ratios in 2024 were *delves* (28×), *underscores* (14×), *showcasing*
  (11×) (Kobak et al. 2025); *delve*, *meticulous* and *commendable* show
  the same acceleration in Scopus abstracts (*Lexical Traces of AI*, 2026).
- **Rate-limit, do not ban** — ordinary academic words whose *rate* is the
  marker: across, additionally, comprehensive, crucial, enhance/enhancing,
  exhibited, findings, insights, notably, particularly, pivotal, potential,
  robust, within (Kobak et al. 2025, common-word excess set). Each is
  defensible once, with a reason. Three in a paragraph is the tell, and the
  concrete alternative is almost always better: "crucial" → what breaks
  without it; "enhance" → the measured delta; "comprehensive" → the
  enumeration; "robust" → the perturbation it survived.
- **Titles.** "beyond" and "via" are both over-represented in post-LLM
  paper titles, and abstracts show depressed rates of "the" and "of"
  (*Beyond Via*, 2026). A title of the shape "X: Beyond Y via Z" now reads
  as generated on sight.
- **Em dash — the strongest punctuation marker measured so far.** In
  medRxiv Discussion sections, prevalence rose from 4.2% pre-ChatGPT to
  8.0% in 2024 and 20.3% in 2025, with no comparable rise in boilerplate
  sections (Czuma 2026). Budget at most one per page, and only where a
  comma, colon, or parentheses genuinely will not serve. In LaTeX, also
  confirm `---` is not standing in where an en dash (ranges) or a hyphen
  (compound modifiers) belongs.

### Decayed or contested — do not rely on these

- **delve** is now a weak discriminator: still avoid it, but its absence
  proves nothing (Geng & Trotta 2025). Much of this vocabulary has also
  diffused into ordinary human usage, including unscripted speech (Anderson
  et al. 2025) — the marker set drifts toward the human baseline over time.
- **Hedging density is not the tell folklore claims.** LLM academic text
  shows *lower* interactional metadiscourse — hedges, boosters, attitude
  markers — than human writing, giving a flatter, more impersonal register
  (Reinhart 2026, surveying the register literature). Stacked hedges remain
  banned under Claims calibration above, for calibration reasons, not as an
  AI tell. If anything, under-hedging is the newer risk.
- **Sentence-initial "Moreover,/Furthermore,/Additionally," spam:** only
  *additionally* is corpus-verified; the other two are inherited folklore.
  Cut all three anyway — they are lazy glue standing where an old-to-new
  content link belongs.

### Structural tics — *observational*

Repeatedly documented by practitioners and community style guides
(Wikipedia's *Signs of AI writing*; Reinhart 2026), but not yet measured in
an academic corpus. Weight them below the lexical evidence, and fix them as
prose faults on their own merits rather than as detector evasion.

- **Negative parallelism:** "it's not just X — it's Y", "not X, but Y",
  "no X, no Y, just Z". Currently the most-cited construction in tell
  spotting. "Not only X but also Y" belongs here too — once per paper, max.
- **Rule-of-three stacking:** adjective triads, and "X, Y, and Z" phrase
  triads that inflate one point into three. One tricolon is rhetoric;
  three in a section is a template.
- **Copula avoidance:** serves as / functions as / stands as / marks /
  represents / boasts, where "is" is right.
- **Participial tail commentary:** a clause ending ", highlighting …",
  ", underscoring …", ", emphasizing …", ", reflecting …" that restates
  the sentence instead of adding a fact. Corpus-adjacent: the *-ing* forms
  of exactly these verbs carry the top measured excess ratios.
- **Over-signposting:** "It is important to note that" (delete);
  sentence-initial "Crucially,/Notably,/Importantly," asserting an
  importance the content should demonstrate.
- **Boilerplate architecture:** a "Challenges and Future Directions"
  section of unfalsifiable speculation; sections ending in summary
  restatement ("Overall, …") — end on new substance.
- **Chat formatting imported into a paper:** bold-header bullets in running
  prose, title-case section headings, emoji, stray markdown. Papers use
  paragraphs and sentence-case headings.
- **Elegant variation** — synonym rotation driven by repetition penalties.
  Both an AI tell and a terminology-consistency bug; same term, every time.

### Uniform prose shape — *observational*

Every sentence 18–25 words with one subordinate clause, every paragraph the
same length, sentence openings drawn from one narrow set. Human academic
prose is bursty. Vary length and construction deliberately, and let some
sentences be short.

- Every "has been shown" needs a \cite; no "studies have shown" hand-waves.

### What the publishers actually check

Elsevier, Springer Nature, and IEEE all require disclosure of generative-AI
use and hold the human authors accountable for every claim in the text;
none of them publishes a reviewer checklist of textual tells. No list here
is an official standard. What this section defends against is reviewer
intuition and publisher screening tooling, both of which move faster than
any published policy — and neither of which you get to argue with.

### Sources

- Kobak, González-Márquez, Horvát, Lause, "Delving into LLM-assisted
  writing in biomedical publications through excess vocabulary", *Science
  Advances* 11(27), 2025 — 15.1M PubMed abstracts, 2010–2024.
  https://www.science.org/doi/10.1126/sciadv.adt3813 (preprint:
  https://arxiv.org/abs/2406.07016)
- Geng & Trotta, "Human-LLM Coevolution: Evidence from Academic Writing",
  2025 — arXiv abstracts; the "delve" decline and the avoidance signal.
  https://arxiv.org/abs/2502.09606
- "Lexical Traces of AI: Linguistic Impact of Generative Tools in Academic
  Abstracts", *Learned Publishing* 39(3), 2026 — 17 lexical items with
  steep 2022–2024 growth in Scopus, offered as probabilistic markers of an
  era-wide lexical shift, explicitly *not* as diagnostic proof of AI use in
  any single article. https://onlinelibrary.wiley.com/doi/10.1002/leap.2067
- "Beyond Via: Analysis and Estimation of the Impact of Large Language
  Models in Academic Papers", 2026 — title- and abstract-level word shifts.
  https://arxiv.org/abs/2603.25638
- Czuma, "Em-ergence of the em-dash: a population-level rise in em-dash
  frequency in medRxiv preprints at the dawn of the large-language-model
  era", 2026 — 69,632 medRxiv preprints, 2020–2025.
  https://arxiv.org/abs/2606.29540
- "Linguistic Characteristics of AI-Generated Text: A Survey", 2025 —
  lower lexical diversity, flatter register, noun/determiner excess.
  https://arxiv.org/abs/2510.05136
- Reinhart, "LLM writing styles" (research notebook, updated 2026-06) —
  register and metadiscourse findings. *Observational synthesis.*
  https://www.refsmmat.com/notebooks/llm-style.html
- Anderson, Galpin, Juzek, "Model Misalignment and Language Change: Traces
  of AI-Associated Language in Unscripted Spoken English", AIES 2025 —
  22.1M words of podcast speech; diffusion into human usage.
  https://arxiv.org/abs/2508.00238
- Wikipedia, "Signs of AI writing" — the structural-tic catalogue.
  *Community documentation, observational.*
  https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- Elsevier, "Generative AI policies for journals" — disclosure and
  accountability requirements; no reviewer tell-checklist.
  https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals

## Revision passes (in order)

1. Structure: does skimming first sentences of each paragraph reconstruct
   the argument?
2. Claims: every contribution claim → evidence section; every verb matched
   to its evidence; every adjective of degree replaced by a number.
3. Terminology: grep for synonyms of key terms; unify.
4. Lint: banned words, LLM tells, articles, hyphenation, i.e./e.g.
5. Read the abstract and intro out loud last — reviewers judge English there
   first, and calibrate their scrutiny accordingly.
