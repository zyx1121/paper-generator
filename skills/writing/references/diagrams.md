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
- [ ] caption states what the reader should see, not just what the figure is
- [ ] styles defined once; fonts not below `\scriptsize`; no decoration
