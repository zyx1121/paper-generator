---
name: ideation
description: >
  Stage 1 of the paper pipeline: discuss and sharpen a raw research idea into
  a proposal with one key insight, refutable contribution claims, and a
  novelty scan against arXiv. Use when starting a new paper or when the
  current idea needs re-scoping.
---

# Stage 1 — Ideation

Goal: turn a raw idea into `paper/proposal.md` the user signs off on.
This stage is a conversation, not a monologue — short turns, real questions.

## 1. Understand the idea

Ask only what you cannot infer, in at most two rounds:

- What problem does this solve, and for whom? What breaks today without it?
- What is the suspected insight — the one thing that makes this work where
  prior approaches don't?
- What resources exist? (testbed, GPUs, datasets, existing codebase, lab
  infrastructure) — this bounds what kind of paper is feasible.
- Any constraints: deadline, target community, advisor preferences.

## 2. Novelty scan

Before investing anything, check the idea against the literature:

- `arxiv_search` with 2–3 query formulations (problem phrasing, technique
  phrasing, fielded queries like `ti:"..." AND cat:cs.NI`), sorted by
  relevance and by `submittedDate` for the recent frontier.
- WebSearch for the obvious name of the idea plus "paper" — catches venue
  publications arXiv misses.
- For the 3–5 closest hits, read the abstracts carefully and write one
  sentence each: what they do, and what this idea does that they do not.

Outcomes:
- **Clear** — proceed.
- **Close prior work exists** — tell the user plainly, propose a
  differentiated angle (new setting, new constraint, order-of-magnitude
  improvement) or recommend dropping it. Do not talk the user into a paper
  that is a rediscovery.

## 3. Sharpen to one ping

A paper carries exactly one key idea (Peyton Jones). Force the idea through
this sentence until it is sharp:

> The main idea of this paper is ____.

Then draft **contributions as refutable claims** — each one something a
reviewer could check and potentially falsify, each one implying the evidence
that will back it:

- Bad: "We describe the WizWoz system. It is really cool."
- Good: "We design X, the first Y that Z under constraint W (§3)."
- Good: "X improves p99 latency by Nx over <best baseline> on <workloads> (§5)."

3–4 claims is typical. Every claim must be one the planned experiments can
actually substantiate — if you cannot imagine the graph that proves a claim,
cut or reword the claim now, not in Stage 6.

## 4. Write proposal.md

```markdown
# <working title>
## Problem            — 2–3 sentences, concrete, with an example
## Key insight        — "The main idea of this paper is ..."
## Contributions      — refutable claims, each with its planned evidence
## Closest prior work — 3–5 entries: citation, what it does, how we differ
## Feasibility        — what we build, what we measure, what resources it needs
## Risks              — what could kill this (and the fallback if it does)
```

## Gate G1

Present the proposal, flag the biggest risk yourself, and give your honest
read on whether this is a workshop idea or a full-conference idea. Wait for
the user's approval or edits. Record the outcome in `paper/STATE.md`.
