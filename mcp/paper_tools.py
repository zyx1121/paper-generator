#!/usr/bin/env python3
"""paper-tools — zero-dependency MCP stdio server for the paper-generator plugin.

Tools:
  latex_compile  — compile a LaTeX project to PDF (latexmk / tectonic / pdflatex),
                   parse the log into structured errors, warnings, and page count
  render_figure  — run a Python figure script headlessly (MPLBACKEND=Agg) and
                   report the image files it produced
  arxiv_search   — search the arXiv API (novelty / related-work scouting)
  scholar_search — search Semantic Scholar (OpenAlex fallback): published
                   venues, citation counts, open-access PDF links
  dblp_bibtex    — search DBLP and return ready-to-paste BibTeX entries

Requires only the Python 3.9+ standard library. Network is used only by
arxiv_search / scholar_search / dblp_bibtex.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

SERVER_NAME = "paper-tools"
SERVER_VERSION = "0.1.0"
PROTOCOL_VERSION = "2024-11-05"

USER_AGENT = f"{SERVER_NAME}/{SERVER_VERSION} (paper-generator Claude Code plugin)"


# ---------------------------------------------------------------- LaTeX

LOG_ERROR_RE = re.compile(r"^! (.+)$", re.MULTILINE)
LOG_LINE_RE = re.compile(r"^l\.(\d+)", re.MULTILINE)
MISSING_REF_RE = re.compile(r"LaTeX Warning: Reference `([^']+)' .* undefined")
MISSING_CITE_RE = re.compile(r"LaTeX Warning: Citation `([^']+)' .* undefined")
OVERFULL_RE = re.compile(r"^Overfull \\hbox \(([\d.]+)pt too wide\)", re.MULTILINE)
PAGES_RE = re.compile(r"Output written on .+\((\d+) pages?")


def _run(cmd, cwd, timeout, env=None):
    merged_env = dict(os.environ)
    if env:
        merged_env.update(env)
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, timeout=timeout, env=merged_env,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
            errors="replace",
        )
        return proc.returncode, proc.stdout
    except subprocess.TimeoutExpired:
        return -1, f"TIMEOUT after {timeout}s: {' '.join(cmd)}"
    except FileNotFoundError:
        return -2, f"NOT FOUND: {cmd[0]}"


def _parse_latex_log(log_text):
    errors = []
    for m in LOG_ERROR_RE.finditer(log_text):
        # Grab the error line plus the l.<n> context that usually follows.
        tail = log_text[m.end():m.end() + 400]
        line_m = LOG_LINE_RE.search(tail)
        errors.append({
            "message": m.group(1).strip(),
            "line": int(line_m.group(1)) if line_m else None,
        })
    overfull = OVERFULL_RE.findall(log_text)
    pages_m = None
    for pages_m in PAGES_RE.finditer(log_text):
        pass  # keep the last occurrence
    return {
        "errors": errors[:20],
        "undefined_references": sorted(set(MISSING_REF_RE.findall(log_text)))[:30],
        "undefined_citations": sorted(set(MISSING_CITE_RE.findall(log_text)))[:30],
        "overfull_hboxes": {
            "count": len(overfull),
            "worst_pt": max((float(x) for x in overfull), default=0.0),
        },
        "pages": int(pages_m.group(1)) if pages_m else None,
    }


def tool_latex_compile(args):
    project_dir = os.path.abspath(os.path.expanduser(args["project_dir"]))
    main_tex = args.get("main_tex", "main.tex")
    engine = args.get("engine", "auto")
    timeout = int(args.get("timeout", 300))

    tex_path = os.path.join(project_dir, main_tex)
    if not os.path.isfile(tex_path):
        return {"ok": False, "error": f"main tex file not found: {tex_path}"}

    base = os.path.splitext(os.path.basename(main_tex))[0]

    def has(prog):
        return shutil.which(prog) is not None

    if engine == "auto":
        if has("latexmk"):
            engine = "latexmk"
        elif has("tectonic"):
            engine = "tectonic"
        elif has("pdflatex"):
            engine = "pdflatex"
        else:
            return {"ok": False, "error": (
                "no LaTeX toolchain found (tried latexmk, tectonic, pdflatex). "
                "Install TeX Live (`sudo apt install texlive-full latexmk`) or "
                "tectonic (`cargo install tectonic` / brew install tectonic)."
            )}

    started = time.time()
    if engine == "latexmk":
        rc, out = _run(
            ["latexmk", "-pdf", "-interaction=nonstopmode", "-file-line-error",
             f"-jobname={base}", main_tex],
            project_dir, timeout)
    elif engine == "tectonic":
        rc, out = _run(["tectonic", "--keep-logs", main_tex], project_dir, timeout)
    elif engine == "pdflatex":
        # pdflatex x2 with the bibliography tool in between if a .bib is used:
        # biber for biblatex (\addbibresource), classic bibtex otherwise
        rc, out = _run(["pdflatex", "-interaction=nonstopmode",
                        "-file-line-error", main_tex], project_dir, timeout)
        src = open(tex_path, errors="replace").read()
        if rc == 0 and re.search(r"\\bibliography\b|\\addbibresource", src):
            bib_tool = "biber" if "\\addbibresource" in src else "bibtex"
            for cmd in ([bib_tool, base],
                        ["pdflatex", "-interaction=nonstopmode", main_tex],
                        ["pdflatex", "-interaction=nonstopmode", main_tex]):
                rc2, out2 = _run(cmd, project_dir, timeout)
                out += "\n" + out2
            rc = rc2
    else:
        return {"ok": False, "error": f"unknown engine: {engine}"}

    log_path = os.path.join(project_dir, base + ".log")
    log_text = ""
    if os.path.isfile(log_path):
        with open(log_path, errors="replace") as f:
            log_text = f.read()
    parsed = _parse_latex_log(log_text or out)

    pdf_path = os.path.join(project_dir, base + ".pdf")
    ok = rc == 0 and os.path.isfile(pdf_path) and not parsed["errors"]
    result = {
        "ok": ok,
        "engine": engine,
        "pdf": pdf_path if os.path.isfile(pdf_path) else None,
        "seconds": round(time.time() - started, 1),
        **parsed,
    }
    if not ok and not parsed["errors"]:
        result["raw_tail"] = out[-2000:]
    return result


# ---------------------------------------------------------------- figures

IMG_EXTS = (".pdf", ".png", ".svg", ".eps", ".jpg", ".jpeg")


def tool_render_figure(args):
    script = os.path.abspath(os.path.expanduser(args["script"]))
    cwd = os.path.abspath(os.path.expanduser(args.get("cwd", os.path.dirname(script))))
    timeout = int(args.get("timeout", 120))
    python = args.get("python", sys.executable or "python3")

    if not os.path.isfile(script):
        return {"ok": False, "error": f"script not found: {script}"}

    before = {}
    for root, _dirs, files in os.walk(cwd):
        for f in files:
            if f.lower().endswith(IMG_EXTS):
                p = os.path.join(root, f)
                before[p] = os.path.getmtime(p)

    rc, out = _run([python, script], cwd, timeout, env={"MPLBACKEND": "Agg"})

    produced = []
    for root, _dirs, files in os.walk(cwd):
        for f in files:
            if f.lower().endswith(IMG_EXTS):
                p = os.path.join(root, f)
                if p not in before or os.path.getmtime(p) > before[p]:
                    produced.append(p)

    return {
        "ok": rc == 0,
        "exit_code": rc,
        "produced_files": sorted(produced),
        "output": out[-3000:],
    }


# ---------------------------------------------------------------- arXiv

ATOM = "{http://www.w3.org/2005/Atom}"


def _http_get(url, timeout=30, headers=None):
    merged = {"User-Agent": USER_AGENT}
    if headers:
        merged.update(headers)
    req = urllib.request.Request(url, headers=merged)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def tool_arxiv_search(args):
    query = args["query"]
    max_results = min(int(args.get("max_results", 10)), 30)
    url = ("http://export.arxiv.org/api/query?" + urllib.parse.urlencode({
        "search_query": query if ":" in query else f"all:{query}",
        "start": 0, "max_results": max_results,
        "sortBy": args.get("sort_by", "relevance"),
    }))
    try:
        body = _http_get(url)
        root = ET.fromstring(body)
    except Exception as e:  # noqa: BLE001 — report any fetch/parse failure to the model
        return {"ok": False, "error": f"arxiv query failed: {e}"}

    papers = []
    for entry in root.findall(ATOM + "entry"):
        def txt(tag, e=entry):
            el = e.find(ATOM + tag)
            return (el.text or "").strip() if el is not None else ""
        arxiv_id = txt("id").rsplit("/", 1)[-1]
        papers.append({
            "id": arxiv_id,
            "title": re.sub(r"\s+", " ", txt("title")),
            "authors": [
                (a.find(ATOM + "name").text or "").strip()
                for a in entry.findall(ATOM + "author")
            ],
            "published": txt("published")[:10],
            "abstract": re.sub(r"\s+", " ", txt("summary"))[:1200],
            "url": f"https://arxiv.org/abs/{arxiv_id}",
        })
    return {"ok": True, "count": len(papers), "papers": papers}


# ------------------------------------------- scholarly search (S2 + OpenAlex)

S2_FIELDS = ("title,abstract,venue,year,citationCount,authors,"
             "externalIds,openAccessPdf,url")


def _s2_search(query, limit):
    url = ("https://api.semanticscholar.org/graph/v1/paper/search?" +
           urllib.parse.urlencode({
               "query": query, "limit": limit, "fields": S2_FIELDS,
           }))
    # The keyless shared pool rate-limits aggressively; a free key from
    # https://www.semanticscholar.org/product/api lifts it.
    headers = {}
    if os.environ.get("S2_API_KEY"):
        headers["x-api-key"] = os.environ["S2_API_KEY"]
    data = json.loads(_http_get(url, headers=headers))

    papers = []
    for p in data.get("data") or []:
        ext = p.get("externalIds") or {}
        oa = p.get("openAccessPdf") or {}
        papers.append({
            "title": p.get("title"),
            "authors": [a.get("name") for a in p.get("authors") or []][:12],
            "year": p.get("year"),
            "venue": p.get("venue") or None,
            "citations": p.get("citationCount"),
            "doi": ext.get("DOI"),
            "arxiv": ext.get("ArXiv"),
            "pdf": oa.get("url"),
            "abstract": (p.get("abstract") or "")[:1200] or None,
            "url": p.get("url"),
        })
    return {"ok": True, "source": "semantic_scholar",
            "total": data.get("total"),
            "count": len(papers), "papers": papers}


def _openalex_search(query, limit):
    url = ("https://api.openalex.org/works?" + urllib.parse.urlencode({
        "search": query, "per-page": limit,
        "select": ("title,publication_year,cited_by_count,doi,ids,"
                   "primary_location,best_oa_location,authorships,"
                   "abstract_inverted_index"),
    }))
    data = json.loads(_http_get(url))

    papers = []
    for w in data.get("results") or []:
        # OpenAlex ships abstracts as an inverted index; reconstruct.
        pos_to_word = {}
        for word, positions in (w.get("abstract_inverted_index") or {}).items():
            for pos in positions:
                pos_to_word[pos] = word
        abstract = " ".join(pos_to_word[i] for i in sorted(pos_to_word))
        source = (w.get("primary_location") or {}).get("source") or {}
        oa = w.get("best_oa_location") or {}
        papers.append({
            "title": w.get("title"),
            "authors": [(a.get("author") or {}).get("display_name")
                        for a in w.get("authorships") or []][:12],
            "year": w.get("publication_year"),
            "venue": source.get("display_name"),
            "citations": w.get("cited_by_count"),
            "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
            "arxiv": None,
            "pdf": oa.get("pdf_url"),
            "abstract": abstract[:1200] or None,
            "url": (w.get("ids") or {}).get("openalex"),
        })
    return {"ok": True, "source": "openalex",
            "total": (data.get("meta") or {}).get("count"),
            "count": len(papers), "papers": papers}


def tool_scholar_search(args):
    query = args["query"]
    limit = min(int(args.get("max_results", 10)), 20)

    s2_err = None
    for attempt in range(2):
        try:
            return _s2_search(query, limit)
        except Exception as e:  # noqa: BLE001 — 429s are routine on the keyless pool
            s2_err = e
            if attempt == 0:
                time.sleep(3)
    try:
        return _openalex_search(query, limit)
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": (
            f"semantic scholar failed ({s2_err}); openalex failed ({e})")}


# ---------------------------------------------------------------- DBLP


def tool_dblp_bibtex(args):
    query = args["query"]
    max_results = min(int(args.get("max_results", 5)), 15)
    url = ("https://dblp.org/search/publ/api?" + urllib.parse.urlencode({
        "q": query, "h": max_results, "format": "json",
    }))
    try:
        data = json.loads(_http_get(url))
        hits = data["result"]["hits"].get("hit", [])
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"dblp query failed: {e}"}

    entries = []
    for h in hits:
        info = h.get("info", {})
        key = info.get("key")
        bibtex = None
        if key:
            try:
                bibtex = _http_get(f"https://dblp.org/rec/{key}.bib?param=1").strip()
            except Exception:  # noqa: BLE001
                pass
        entries.append({
            "title": info.get("title"),
            "venue": info.get("venue"),
            "year": info.get("year"),
            "doi": info.get("doi"),
            "bibtex": bibtex,
        })
    return {"ok": True, "count": len(entries), "entries": entries}


# ---------------------------------------------------------------- MCP plumbing

TOOLS = [
    {
        "name": "latex_compile",
        "description": (
            "Compile a LaTeX project to PDF and return structured results: "
            "errors with line numbers, undefined references/citations, overfull "
            "hbox count, page count, and the PDF path. Auto-detects latexmk, "
            "tectonic, or pdflatex. Always use this instead of running latex "
            "commands manually."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_dir": {"type": "string", "description": "Absolute path to the LaTeX project directory"},
                "main_tex": {"type": "string", "description": "Main .tex file relative to project_dir (default: main.tex)"},
                "engine": {"type": "string", "enum": ["auto", "latexmk", "tectonic", "pdflatex"], "description": "Toolchain to use (default: auto)"},
                "timeout": {"type": "integer", "description": "Seconds before aborting (default: 300)"},
            },
            "required": ["project_dir"],
        },
        "handler": tool_latex_compile,
    },
    {
        "name": "render_figure",
        "description": (
            "Run a Python figure-generation script headlessly (MPLBACKEND=Agg) "
            "and report which image files (.pdf/.png/.svg/.eps) it created or "
            "updated, plus its output on failure."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "script": {"type": "string", "description": "Absolute path to the Python script"},
                "cwd": {"type": "string", "description": "Working directory (default: the script's directory)"},
                "python": {"type": "string", "description": "Python interpreter to use (default: the server's interpreter)"},
                "timeout": {"type": "integer", "description": "Seconds before aborting (default: 120)"},
            },
            "required": ["script"],
        },
        "handler": tool_render_figure,
    },
    {
        "name": "arxiv_search",
        "description": (
            "Search arXiv for papers (novelty checks, related work). Query can "
            "be free text or fielded arXiv syntax like 'ti:\"congestion control\" "
            "AND cat:cs.NI'. Returns title, authors, date, abstract, URL."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "max_results": {"type": "integer", "description": "1-30, default 10"},
                "sort_by": {"type": "string", "enum": ["relevance", "submittedDate"], "description": "default relevance"},
            },
            "required": ["query"],
        },
        "handler": tool_arxiv_search,
    },
    {
        "name": "scholar_search",
        "description": (
            "Search scholarly literature (Semantic Scholar, falling back to "
            "OpenAlex) across published venues — coverage arXiv lacks — with "
            "citation counts, venue, year, DOI, and an open-access PDF link "
            "when available. Use alongside arxiv_search in novelty scans; "
            "use citation counts to rank which prior work reviewers will "
            "expect cited."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "max_results": {"type": "integer", "description": "1-20, default 10"},
            },
            "required": ["query"],
        },
        "handler": tool_scholar_search,
    },
    {
        "name": "dblp_bibtex",
        "description": (
            "Search DBLP by title/author keywords and return ready-to-paste "
            "BibTeX entries with venue and year — use this to build the .bib "
            "file instead of hand-writing entries."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "max_results": {"type": "integer", "description": "1-15, default 5"},
            },
            "required": ["query"],
        },
        "handler": tool_dblp_bibtex,
    },
]

TOOLS_BY_NAME = {t["name"]: t for t in TOOLS}


def handle(msg):
    method = msg.get("method")
    msg_id = msg.get("id")
    if method == "initialize":
        return {
            "jsonrpc": "2.0", "id": msg_id,
            "result": {
                "protocolVersion": msg.get("params", {}).get(
                    "protocolVersion", PROTOCOL_VERSION),
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            },
        }
    if method == "tools/list":
        return {
            "jsonrpc": "2.0", "id": msg_id,
            "result": {"tools": [
                {k: t[k] for k in ("name", "description", "inputSchema")}
                for t in TOOLS
            ]},
        }
    if method == "tools/call":
        params = msg.get("params", {})
        tool = TOOLS_BY_NAME.get(params.get("name"))
        if tool is None:
            return {"jsonrpc": "2.0", "id": msg_id,
                    "error": {"code": -32602,
                              "message": f"unknown tool: {params.get('name')}"}}
        try:
            result = tool["handler"](params.get("arguments", {}))
        except Exception as e:  # noqa: BLE001 — surface tool crashes as tool errors
            result = {"ok": False, "error": f"{type(e).__name__}: {e}"}
        return {
            "jsonrpc": "2.0", "id": msg_id,
            "result": {
                "content": [{"type": "text",
                             "text": json.dumps(result, indent=2)}],
                "isError": not result.get("ok", True),
            },
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {}}
    if msg_id is not None:  # unknown request (not a notification)
        return {"jsonrpc": "2.0", "id": msg_id,
                "error": {"code": -32601, "message": f"unknown method: {method}"}}
    return None  # notification — no response


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        resp = handle(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
