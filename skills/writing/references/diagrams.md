# Paper diagram reference (architecture, state, flow)

Data figures — plots generated from experiment data — are covered by the
analysis skill. This reference covers the *drawn* figures: architecture and
system diagrams, state machines, pipelines, and message-sequence charts,
including the Figure 1 most systems papers open with.

## Tool: TikZ, versioned, compiled like everything else

Draw diagrams in TikZ, not in an external drawing tool. Reasons:

- Vector output with embedded fonts, typographically consistent with the
  manuscript — a rasterized or mismatched-font diagram reads as sloppy at
  review zoom.
- The source lives in `paper/figures/<name>.tex`, versioned and diffable;
  renaming a component is an edit, not a re-export.
- The revision loop is fast and fully in-pipeline (see workflow below).

For genuinely graph-shaped figures — dozens of nodes where the topology is
the point — generate with graphviz (`dot -Tpdf`) instead. Below ~10 blocks,
hand layout beats auto layout every time.

## Workflow per diagram

1. One standalone file per diagram: `paper/figures/<name>.tex` with
   `\documentclass[tikz]{standalone}`.
2. Compile it with `latex_compile` (`main_tex` = the diagram file) to get
   `<name>.pdf`.
3. **Read the produced PDF and look at it.** Overlapping nodes, crowded
   labels, arrows crossing text — the log will not tell you; your eyes will.
   Iterate until clean; each cycle is seconds.
4. `\includegraphics` it from the manuscript like any other figure.

A trivial one-off diagram may live inline as a `tikzpicture` in the section
file; move it to standalone the moment iteration gets slow.

Font note: `standalone` defaults to Computer Modern. When the venue class
sets another text font, load the same font package in the diagram preamble
(acmart → `\usepackage{libertine}`) so labels match body text.

## Form follows the question

| To show | Draw |
|---|---|
| components and how data moves | block diagram, left-to-right or top-down |
| a pipeline of stages | horizontal flow, one block per stage |
| lifecycle or protocol states | state machine (`automata` library) |
| who talks to whom over time | message-sequence chart (lifelines + arrows) |
| deployment or trust boundaries | block diagram + dashed `fit` boxes |

## Field figure vocabulary

The rules above are field-independent; *what* to draw, and how much of it, is
not. The authority is the venue profile recorded in `paper/venue.md` (see
`venues/README.md`) — where it disagrees with this section, the profile wins.
This is the at-a-glance version for while you are drawing, and it covers data
figures too, because the figure/table mix is one decision, not two.

**Systems** (OSDI, SOSP, ATC, EuroSys; ICDCS, Middleware). Figure 1 is an
architecture overview or a motivating measurement, and must be comprehensible
alone. Observed range: 12–19 figures with 0–1 tables — specs live in prose at
the USENIX tier, while the IEEE tier adds a results table. Line charts for
latency-vs-load, bars for memory and cost, CDFs inside deep-dive subsections.
**Captions are descriptive labels, not claim sentences**; the finding is
stated in prose before the figure is walked.

**Networking** (SIGCOMM, NSDI, MobiCom, MobiSys, INFOCOM). Figure 1 is a
two-panel contrast: "(a) Conventional [fails] (b) OurSystem [works]".
Figure-heavy and table-light — one SIGCOMM paper ran 16 figures and 0 tables;
tables appear only for dense numeric grids. CDF culture is real: plot the
distribution and name the median in prose. Variance is drawn, not asserted —
shaded ±std bands, 2D std ellipses for two-axis scatter, and an integer run
count in the caption or text ("100 experiments"), never "several runs".
Captions here often add a one-line takeaway after the descriptive label.

**ML** (NeurIPS, ICML, ICLR). Figure 1 is a **teaser** — mechanism sketch,
pipeline contrast, or a display of the phenomenon being challenged — and has
to sell the idea before any result appears. The main results **table** is the
load-bearing item (bold best, ±std over seeds); figures are multi-panel
comparison curves and overlaid predicted-vs-actual lines. Single-column
format: design full-width figures at ≈5.5in, not the 3.3in `\columnwidth`
the style rules below assume.

**Security** (S&P, USENIX Sec, CCS, NDSS). Split by subtype. Tool papers open
with a pipeline diagram and are carried by a large capability-comparison
table with a symbol legend (✓/✗) defined in the caption, plus an enumerated
per-case failure list *(uncertain — one tool paper read)*. Attack papers open
with an attack-flow or protocol-message diagram (an MSC fits) and put
distribution plots in the separate deployment-measurement section. Figures are
a known anonymization leak: no author-identifying paths, and no full CVE
numbers in the review version.

**SE** (ICSE, FSE, ASE). Result **tables keyed to the RQs** are the primary
display items and figures are secondary: a tool/pipeline diagram, plus per-RQ
distribution plots *(uncertain — thin sample)*. Every display item should be
reachable from an RQ; an unattached figure reads as padding here.

**HCI** (CHI, UIST, CSCW). Artifact papers are screenshot-driven: annotated UI
captures plus a walkthrough figure whose step numbers match the numbered
operation steps in the System section. Qualitative papers run figure-light —
a method or timeline diagram and little else, because quotes are the evidence
*(uncertain — pattern from 2 papers)*. Single-column, so full text width.

**Journals**. Nature/Science: **≤6 display items total**, a hard budget that
forces panel merging; legends under 250 words and self-contained, since they
carry method detail the main text drops. IEEE/ACM Transactions: figures skew
architectural and diagrammatic rather than photographic, matching the strict
IMRaD body.

## Style rules

- **Define styles once** with a `block/.style` list in the picture options;
  per-node ad-hoc styling drifts exactly like synonym rotation in prose.
- Font `\small` or `\footnotesize` at final physical size (design the figure
  at `\columnwidth` ≈ 3.3in, like data figures); never below `\scriptsize`.
- Fills light, strokes dark, text black — same colorblind-safe palette as
  the data figures, and the distinction must survive grayscale (vary
  lightness, not just hue).
- Arrows via `arrows.meta` (`-{Stealth}`). Label every arrow whose meaning
  is not obvious. If solid vs. dashed encodes a distinction (data vs.
  control path), state it in the caption.
- Group related components with a dashed `fit` box and a small label —
  machine, process, and trust boundaries earn their ink; decoration does not.
- **No shadows, gradients, 3D, clipart, or icon packs.** Boxes, arrows,
  text.
- Number the steps of the main flow with small circled badges
  (`\node[circle, draw, inner sep=1pt, font=\scriptsize]`) and walk the same
  numbers in prose: "the planner receives the query (①), …". This is what
  makes Figure 1 carry the intro.

## Worked example — block architecture

```latex
\documentclass[tikz]{standalone}
\usetikzlibrary{positioning, arrows.meta, fit}
\begin{document}
\begin{tikzpicture}[
  font=\small, node distance=8mm and 10mm,
  block/.style={draw, rounded corners=2pt, align=center,
                minimum height=2.2em, minimum width=5.5em, fill=blue!8},
  store/.style={block, fill=orange!15},
  flow/.style={-{Stealth[length=2mm]}, semithick},
  note/.style={font=\scriptsize, midway, above},
]
  \node[block] (client) {Client};
  \node[block, right=of client] (planner) {Planner};
  \node[block, right=of planner] (exec) {Executor};
  \node[store, below=of exec] (log) {Write-ahead\\log};

  \draw[flow] (client) -- node[note] {query} (planner);
  \draw[flow] (planner) -- node[note] {plan} (exec);
  \draw[flow] (exec) -- (log);
  \draw[flow, dashed] (log) -| node[note, near start] {recovery} (planner);

  \node[draw, dashed, rounded corners, inner sep=6pt,
        fit=(planner)(exec)(log),
        label={[font=\scriptsize]above:server}] {};
\end{tikzpicture}
\end{document}
```

## State machines

Use the `automata` library; label edges `event / action`:

```latex
\usetikzlibrary{automata, positioning, arrows.meta}
% ...
\begin{tikzpicture}[shorten >=1pt, node distance=2.6cm, auto,
    every state/.style={font=\small, minimum size=2em}]
  \node[state, initial]   (idle) {Idle};
  \node[state]            (act) [right=of idle] {Active};
  \node[state, accepting] (done) [right=of act] {Done};
  \path[-{Stealth}]
    (idle) edge node {req / alloc} (act)
    (act)  edge [loop above] node {tick / renew} (act)
    (act)  edge node {fin / free} (done);
\end{tikzpicture}
```

## Message-sequence charts

Hand-roll with the same primitives: one vertical dashed line per party
(lifeline), horizontal `-{Stealth}` arrows for messages in time order,
message names as `note`-style labels. Time flows down; number the messages
if the prose walks through them.

## Self-check before placing in the manuscript

- [ ] Read the compiled PDF at final size — labels legible, nothing
      overlaps, arrows don't cross text
- [ ] survives grayscale; not readable by hue alone
- [ ] every meaningful arrow labeled; solid/dashed distinction captioned
- [ ] referenced from the text, with a prose walkthrough that follows the
      numbered steps
- [ ] caption follows the field's convention — descriptive label or label
      plus takeaway line (see field vocabulary above / the venue profile)
- [ ] styles defined once; fonts not below `\scriptsize`; no decoration
