---
name: ideation
description: >
  Stage 1 of the paper pipeline: discuss and sharpen a raw research idea into
  a proposal with one key insight, refutable contribution claims, and a
  novelty scan against both the academic indexes and the field's
  non-academic prior art. Use when starting a new paper or when the
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

Before investing anything, check the idea against the literature.

### 2a. Baseline scan — every field

- `arxiv_search` with 2–3 query formulations (problem phrasing, technique
  phrasing, fielded queries like `ti:"..." AND cat:cs.NI`), sorted by
  relevance and by `submittedDate` for the recent frontier.
- `scholar_search` with the same queries — it covers published venues arXiv
  misses and returns citation counts; the high-citation hits are the prior
  work reviewers will expect to see cited and differentiated.
- WebSearch for the obvious name of the idea plus "paper" — catches whatever
  both indexes miss.
- For the 3–5 closest hits, go past the abstract: fetch the paper itself
  (the `pdf` link from `scholar_search`, or the arXiv page) and read at
  least the introduction and contributions. Then write one sentence each:
  what they do, and what this idea does that they do not.

### 2b. Field-specific sources — do not skip

The academic indexes are the floor of the scan, not the scan. Every field
hides its closest prior work somewhere else. Pick the block matching the
target field (same taxonomy as `skills/writing/references/venues/`; for
anything outside it, run the nearest block) and search those sources too
before declaring anything clear.

**Systems / cloud** — industry ships before it publishes, so search code
first:

- GitHub search by topic and by stars (`topic:<keyword>`, sort by stars);
  read the README of anything sizable in the space, not just the title.
- CNCF landscape, plus the sandbox/incubating project lists.
- Engineering blogs of the vendors who run the workload at scale (AWS,
  Google, Meta, Cloudflare, Netflix).
- Kubernetes SIG and working-group repos, and their KEPs, for anything
  cluster-side.

Rationale, from a real failure: on the torpor paper the closest prior work
was **zeropod**, a containerd shim living on GitHub with no paper attached.
The Stage 1 scan hit three academic indexes and missed it; a simulated
reviewer surfaced it in Stage 7, review round 3, with the novelty claim
already written. An unpublished shim is still prior art to a reviewer.

**ML**

- arXiv restricted to the last 12 months, sorted by `submittedDate` — this
  is where the field actually moves; a scan anchored on 3-year-old work is
  not a scan.
- OpenReview, including rejected and withdrawn submissions: a rejected ICLR
  paper still establishes and date-stamps the idea.
- Papers with Code, and the leaderboard page of whichever benchmark the
  planned experiments will use.

**Networking / mobile**

- Standards documents: IEEE 802.11 amendments, 3GPP TSG specs and TRs, IETF
  RFCs and drafts. Mechanisms are routinely standardized before — or
  instead of — being published as papers.
- Public measurement datasets and testbed traces. An existing dataset can
  pre-empt a measurement contribution outright.

**Security**

- CVE / NVD for the vulnerability class, and vendor security advisories for
  whether it is already known and patched.
- DEF CON, Black Hat and CCC programs — practitioner venues disclose ahead
  of the academic write-up.
- Exploit databases (Exploit-DB, Metasploit modules) for whether a working
  attack is already public.

**SE**

- Replication and artifact packages: the ICSE/FSE artifact tracks, plus
  Zenodo and figshare deposits. Tool prototypes often exist there attached
  to someone else's paper, or to no paper at all.
- The candidate tool's own repo and issue tracker for what the maintainers
  already claim.

**HCI**

- ACM DL full-text search is the primary index here; arXiv coverage of
  CHI/UIST/CSCW is low, so an arXiv-first scan under-reports this field
  (*uncertain: no coverage measurement taken — treat as a reason to add
  ACM DL, not as a number*).
- UIST demo/poster tracks and video figures, for interaction techniques
  that never became full papers.

### 2c. Failure modes

- **Scanning only the academic indexes.** The scan misses industry prior
  art — repos, shims, internal systems written up as blog posts, standards
  drafts — and novelty collapses later, when the paper is written and the
  claim is expensive to retract. If the field's block above was not run,
  the scan is incomplete; say so rather than reporting "clear".
- **Not recording what was searched.** Record the scan in `proposal.md`:
  sources queried, date, and what each ruled out. Later stages read it from
  there — related work in Stage 6, the reviewer personas in Stage 7 — and
  will re-derive it badly if it is missing.

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
## Novelty scan       — sources searched + date, what each ruled out, what was
                        skipped (baseline and field-specific sources both)
## Feasibility        — what we build, what we measure, what resources it needs
## Risks              — what could kill this (and the fallback if it does)
```

## Gate G1

Present the proposal, flag the biggest risk yourself, and give your honest
read on whether this is a workshop idea or a full-conference idea. Wait for
the user's approval or edits. Record the outcome in `paper/STATE.md`.
