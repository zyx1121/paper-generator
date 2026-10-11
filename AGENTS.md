# paper-generator

Claude Code plugin: a 9-stage pipeline from a research idea to a submitted paper. Skills are in `skills/`, agents in `agents/`, and the MCP server is `mcp/paper_tools.py`. Read [README.md](README.md) first.

## Rules

- Never fabricate data. Each number in a paper must trace to a run in `paper/experiments/` with its provenance. No user override.
- Gates stop the pipeline for the user. Do not let a stage pass a gate on its own.
- Each hard format fact in a venue profile has a `Facts verified:` date and a primary source. Mark a fact as uncertain when there is no source.
- `mcp/paper_tools.py` uses the Python standard library only. Do not add dependencies.
- `trace_check` and `style_lint` flag problems and change nothing.
- Repository documents and code comments are English.

## Verify

```sh
python3 scripts/ci_checks.py
```

It checks links, cross-references, the plugin manifest, skill frontmatter, Python syntax and the MCP self-tests. CI runs the same script.
