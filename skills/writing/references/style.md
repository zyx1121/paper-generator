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

Because this prose is generated, reviewers and readers will be alert to
these. Treat each as a lint error:

- **Vocabulary:** delve, showcase, underscore, leverage (→use), robust (as
  filler), seamless, holistic, multifaceted, pivotal, crucial, paramount,
  landscape, realm, tapestry, testament, foster, elevate, navigate,
  compelling, groundbreaking, "valuable insights", "plays a vital role",
  "cannot be overstated", "marks a significant shift".
- **Structural tics:** "not only X but also Y" (once per paper, max);
  adjective triads; "serves as / functions as / represents" where "is" is
  right; sentence-initial "Moreover,/Furthermore,/Additionally," spam —
  connect via old-to-new content links instead; "It is important to note
  that" (delete); sections ending in summary restatement ("Overall, …") —
  end on new substance; bold-header bullets in running prose — papers use
  paragraphs; em-dash as universal punctuation.
- **Uniform sentence shape** (every sentence 18–25 words, one subordinate
  clause) — deliberately vary.
- Synonym rotation for technical terms is both an AI tell and a
  terminology-consistency bug — same term, every time.
- Every "has been shown" needs a \cite; no "studies have shown" hand-waves.

## Revision passes (in order)

1. Structure: does skimming first sentences of each paragraph reconstruct
   the argument?
2. Claims: every contribution claim → evidence section; every verb matched
   to its evidence; every adjective of degree replaced by a number.
3. Terminology: grep for synonyms of key terms; unify.
4. Lint: banned words, LLM tells, articles, hyphenation, i.e./e.g.
5. Read the abstract and intro out loud last — reviewers judge English there
   first, and calibrate their scrutiny accordingly.
