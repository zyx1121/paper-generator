# paper-generator

A [Claude Code](https://code.claude.com) plugin that runs a full
**idea → paper** pipeline: discuss and sharpen a research idea, pick a target
venue, set up the experiment environment, implement, run experiments, analyze
results, write a LaTeX paper in professional academic prose, and iterate
through simulated peer review until every reviewer accepts.

```mermaid
flowchart LR
    idea([idea]) --> ideation
    ideation -->|"G1 proposal"| setup
    setup -->|"G2 venue · plan"| implementation
    implementation -->|"G3 artifact"| experiments
    experiments -->|"G4 results"| analysis
    analysis --> writing
    writing -->|"G5 draft"| review["review loop"]
    review -->|"G6 all accept"| finalize
    finalize --> pdf([pdf])
    review -.->|"must-fix → back to any stage"| implementation
```

## Install

```
/plugin marketplace add zyx1121/paper-generator
/plugin install paper-generator@paper-generator
```

Requirements on your machine:

- **Python 3.9+** (`python3` on PATH) — runs the bundled MCP server.
- **A LaTeX toolchain** — `latexmk` (TeX Live) or `tectonic`. The pipeline
  checks and tells you what to install if missing.
- `matplotlib` in whatever Python your figure scripts use.

## Use

```
/paper-generator:paper distributed key-value store that <your idea>
```

Then talk. The pipeline pauses at six gates (proposal, venue + environment +
plan, implementation, results, draft, final sign-off) and runs autonomously
between them. State persists in `paper/STATE.md` in your project — run
`/paper-generator:paper` with no arguments in a later session to resume.

Individual stages are skills too, usable standalone:
`ideation`, `setup`, `implementation`, `experiments`, `analysis`, `writing`,
`review` (mock-review any draft), `finalize` — all under the
`paper-generator:` prefix.

## What's inside

| Component | What it does |
|---|---|
| `skills/paper` | Pipeline orchestrator: stages, gates, state protocol, integrity rules |
| `skills/<stage>` | Detailed procedure for each of the eight stages |
| `skills/writing/references/structure.md` | CS paper structure distilled from Peyton Jones, Widom, SIGPLAN guidelines, venue author guides |
| `skills/writing/references/style.md` | Prose rulebook: voice, information flow, terminology, claims calibration, banned words, LLM-tell counter-programming |
| `skills/writing/references/diagrams.md` | Drawn figures (architecture / state / flow) in TikZ: standalone workflow, style rules, compile-and-look loop |
| `agents/reviewer` | Simulated PC reviewer (three personas: domain expert, methods hawk, informed outsider) with a structured review form |
| `agents/copyeditor` | In-place prose editor that enforces the style rulebook without touching technical content |
| `mcp/paper_tools.py` | Zero-dependency MCP server: `latex_compile` (structured errors, page count), `render_figure`, `arxiv_search`, `scholar_search` (Semantic Scholar → OpenAlex; citation counts, OA PDFs), `dblp_bibtex` |

## Principles baked in

- **No fabricated data, ever.** Every number in the paper must trace to a
  real run under `paper/experiments/`, with per-run provenance (command,
  config, seed, environment, commit hash). This rule has no user override.
- **Gates are hard stops.** Irreversible or judgment calls go to you, with a
  recommendation attached; everything between gates is autonomous.
- **Claims are refutable.** Contributions are written as checkable claims,
  each forward-referenced to the evidence that substantiates it — and the
  review loop attacks exactly that mapping.

## License

MIT
