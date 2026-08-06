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
  fetch_paper    — fetch a paper's full text (arXiv HTML → ar5iv → PDF, or any
                   URL) with mirror and User-Agent fallbacks
  trace_check    — mechanical no-fabrication audit: every number in the .tex
                   sources that has no match in the evidence files

Requires only the Python 3.9+ standard library. Network is used only by
arxiv_search / scholar_search / dblp_bibtex / fetch_paper. `pdftotext`
(poppler) is an optional external binary used by fetch_paper for PDF sources.

Run `python3 paper_tools.py --self-test` for the offline unit tests.
"""

import bisect
import html.parser
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
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

    # Keyless, the shared S2 pool is rate-limited to near-uselessness
    # (observed 0/3 success in real sessions): one shot, no sleep, fall
    # through to OpenAlex. With a key, a retry is worth the wait.
    attempts = 2 if os.environ.get("S2_API_KEY") else 1
    s2_err = None
    for attempt in range(attempts):
        try:
            return _s2_search(query, limit)
        except Exception as e:  # noqa: BLE001 — 429s are routine
            s2_err = e
            if attempt < attempts - 1:
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


# ---------------------------------------------------------------- full text

# Real-world breakage this works around:
#   * arxiv.org/html/<id> only exists for papers submitted from ~Dec 2023 on;
#     anything older 404s and has to go through ar5iv.
#   * ar5iv silently 302s to arxiv.org/abs/<id> when it has no rendition, so a
#     200 is not enough — the final URL has to be checked.
#   * usenix.org (and several publisher hosts) 403 a non-browser User-Agent.
#   * dl.acm.org 403s everything that is not a real browser; nothing here fixes
#     that, so it is reported as a dead end with a suggested workaround.
BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/125.0.0.0 Safari/537.36")
UA_BLOCK_STATUSES = (401, 403, 406, 429)
MAX_DOWNLOAD_BYTES = 25 * 1024 * 1024
MIN_USEFUL_CHARS = 400  # below this a "200 OK" is almost always a stub page

POPPLER_HINT = ("install poppler for PDF extraction "
                "(`brew install poppler` / `sudo apt install poppler-utils`), "
                "or pass an HTML source such as an ar5iv URL instead")

_ARXIV_NEW = r"\d{4}\.\d{4,5}(?:v\d+)?"
_ARXIV_OLD = r"[a-z][a-z-]+(?:\.[a-z]{2})?/\d{7}(?:v\d+)?"
ARXIV_BARE_RE = re.compile(
    r"^(?:arxiv[:/]\s*)?(%s|%s)$" % (_ARXIV_NEW, _ARXIV_OLD), re.I)
ARXIV_URL_RE = re.compile(
    r"^https?://(?:www\.|export\.)?arxiv\.org/(?:abs|pdf|html|format)/(%s|%s)"
    r"(?:\.pdf)?/?(?:[?#].*)?$" % (_ARXIV_NEW, _ARXIV_OLD), re.I)
AR5IV_URL_RE = re.compile(
    r"^https?://ar5iv(?:\.labs)?\.arxiv\.org/(?:html|abs)/(%s|%s)/?$"
    % (_ARXIV_NEW, _ARXIV_OLD), re.I)


class PdfToolMissing(Exception):
    """pdftotext is not on PATH, so a PDF source cannot be read."""


def _arxiv_id(ref):
    """Return the arXiv id in `ref` (bare id, arXiv URL, ar5iv URL) or None."""
    for pattern in (ARXIV_BARE_RE, ARXIV_URL_RE, AR5IV_URL_RE):
        m = pattern.match(ref.strip())
        if m:
            return m.group(1)
    return None


def _arxiv_sources(arxiv_id):
    """Mirrors to try, in order: native HTML, ar5iv HTML, then the PDF."""
    return [
        f"https://arxiv.org/html/{arxiv_id}",
        f"https://ar5iv.labs.arxiv.org/html/{arxiv_id}",
        f"https://arxiv.org/pdf/{arxiv_id}",
    ]


_VOID_TAGS = {"br", "hr", "img", "meta", "link", "input", "source", "col",
              "area", "base", "embed", "param", "track", "wbr"}
_SKIP_TAGS = {"script", "style", "noscript", "svg", "form", "button", "select"}
_HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
_BLOCK_TAGS = {"p", "div", "section", "article", "li", "ul", "ol", "tr", "td",
               "th", "table", "blockquote", "pre", "figure", "figcaption",
               "dd", "dt", "header", "footer", "nav", "main", "aside"}


class _HtmlTextExtractor(html.parser.HTMLParser):
    """Crude tag-stripper that keeps paragraph and heading structure.

    MathML is replaced by its `alttext` (arXiv and ar5iv both carry the
    original LaTeX there), which keeps formulas readable instead of turning
    them into a soup of loose digits.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self._title_parts = []
        self._stack = []
        self._skip_at = None
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in _VOID_TAGS:
            if tag == "br" and self._skip_at is None:
                self.parts.append("\n")
            return
        self._stack.append(tag)
        if self._skip_at is not None:
            return
        if tag == "math":
            alt = dict(attrs).get("alttext")
            self.parts.append(" $%s$ " % alt.strip() if alt else " ")
            self._skip_at = len(self._stack) - 1
            return
        if tag in _SKIP_TAGS:
            self._skip_at = len(self._stack) - 1
            return
        if tag == "title":
            self._in_title = True
        elif tag in _HEADING_TAGS:
            self.parts.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in _VOID_TAGS:
            return
        if tag in self._stack:  # unwind to the matching open tag
            while self._stack and self._stack.pop() != tag:
                pass
        if self._skip_at is not None:
            if len(self._stack) <= self._skip_at:
                self._skip_at = None
            return
        if tag == "title":
            self._in_title = False
        elif tag in _HEADING_TAGS or tag in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        if self._skip_at is not None:
            return
        (self._title_parts if self._in_title else self.parts).append(data)

    def title(self):
        return re.sub(r"\s+", " ", "".join(self._title_parts)).strip()

    def text(self):
        text = "".join(self.parts)
        text = re.sub(r"[ \t\r\f\v]+", " ", text)
        text = re.sub(r" *\n *", "\n", text)
        return re.sub(r"\n{3,}", "\n\n", text).strip()


def _html_to_text(markup):
    """Return (title_guess, text) for an HTML document."""
    parser = _HtmlTextExtractor()
    try:
        parser.feed(markup)
        parser.close()
    except Exception:  # noqa: BLE001 — malformed markup: keep what we parsed
        pass
    text = parser.text()
    title = parser.title()
    if not title:
        for line in text.split("\n"):
            stripped = line.lstrip("# ").strip()
            if stripped:
                title = stripped[:300]
                break
    return title, text


def _pdf_to_text(data, timeout):
    exe = shutil.which("pdftotext")
    if exe is None:
        raise PdfToolMissing("pdftotext not found on PATH")
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "paper.pdf")
        dst = os.path.join(tmp, "paper.txt")
        with open(src, "wb") as f:
            f.write(data)
        rc, out = _run([exe, "-q", "-enc", "UTF-8", src, dst], tmp, timeout)
        if rc != 0 or not os.path.isfile(dst):
            raise RuntimeError(f"pdftotext failed (rc={rc}): {out[-300:].strip()}")
        with open(dst, errors="replace") as f:
            raw = f.read()
    text = re.sub(r"[ \t]+", " ", raw.replace("\f", "\n\n"))
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    title = ""
    for line in text.split("\n"):
        if line.strip():
            title = line.strip()[:300]
            break
    return title, text


def _http_fetch_raw(url, timeout, user_agent):
    headers = {
        "User-Agent": user_agent,
        "Accept": ("text/html,application/xhtml+xml,application/pdf;q=0.9,"
                   "*/*;q=0.8"),
        "Accept-Language": "en-US,en;q=0.9",
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return {
            "url": resp.geturl(),
            "content_type": (resp.headers.get("Content-Type") or "").lower(),
            "charset": resp.headers.get_content_charset(),
            "data": resp.read(MAX_DOWNLOAD_BYTES + 1),
        }


def _fetch_with_ua_fallback(url, timeout):
    """Fetch `url`, retrying once with a browser User-Agent when blocked."""
    try:
        return _http_fetch_raw(url, timeout, USER_AGENT), None
    except Exception as first:  # noqa: BLE001 — decide from the status code
        status = getattr(first, "code", None)
        retryable = status in UA_BLOCK_STATUSES or isinstance(
            first, urllib.error.URLError) and status is None
        if not retryable:
            raise
        try:
            return (_http_fetch_raw(url, timeout, BROWSER_UA),
                    f"retried with a browser User-Agent after {_describe_error(first)}")
        except Exception:  # noqa: BLE001 — report the original failure
            raise first


def _describe_error(exc):
    if isinstance(exc, urllib.error.HTTPError):
        return f"HTTP {exc.code} {exc.reason}"
    if isinstance(exc, urllib.error.URLError):
        return f"network error: {exc.reason}"
    return f"{type(exc).__name__}: {exc}"


def _failure_hint(url, exc):
    host = urllib.parse.urlparse(url).netloc.lower()
    status = getattr(exc, "code", None)
    if "dl.acm.org" in host and status in UA_BLOCK_STATUSES:
        return ("the ACM Digital Library blocks scripted access even with a "
                "browser User-Agent; use the arXiv/author copy, or the "
                "author-provided PDF linked from scholar_search")
    if status in UA_BLOCK_STATUSES:
        return ("the publisher blocked this request; try an open-access "
                "mirror (arXiv / ar5iv / the author's page)")
    return None


def _extract_document(resp, timeout):
    """Return (kind, title_guess, text) for a fetched response."""
    is_pdf = ("pdf" in resp["content_type"]
              or resp["data"][:5] == b"%PDF-")
    if is_pdf:
        title, text = _pdf_to_text(resp["data"], timeout)
        return "pdf", title, text
    markup = resp["data"].decode(resp["charset"] or "utf-8", errors="replace")
    title, text = _html_to_text(markup)
    return "html", title, text


def tool_fetch_paper(args):
    ref = str(args.get("ref", "")).strip()
    if not ref:
        return {"ok": False, "error": "ref is required (arXiv id, arXiv URL, "
                                      "or any PDF/HTML URL)"}
    max_chars = max(1000, min(int(args.get("max_chars", 40000)), 400000))
    timeout = max(5, min(int(args.get("timeout", 45)), 180))

    arxiv_id = _arxiv_id(ref)
    if arxiv_id:
        candidates = _arxiv_sources(arxiv_id)
    elif re.match(r"^https?://", ref, re.I):
        candidates = [ref]
    else:
        return {"ok": False, "error": (
            f"cannot interpret ref {ref!r}: expected an arXiv id (2401.01234), "
            "an arXiv/ar5iv URL, or an http(s) URL to a PDF or HTML page")}

    attempts = []
    for url in candidates:
        try:
            resp, note = _fetch_with_ua_fallback(url, timeout)
        except Exception as e:  # noqa: BLE001 — a dead mirror is normal
            attempt = {"url": url, "ok": False, "reason": _describe_error(e)}
            hint = _failure_hint(url, e)
            if hint:
                attempt["hint"] = hint
            attempts.append(attempt)
            continue

        if len(resp["data"]) > MAX_DOWNLOAD_BYTES:
            attempts.append({"url": url, "ok": False, "reason": (
                f"response exceeds the {MAX_DOWNLOAD_BYTES // (1024 * 1024)} MB "
                "download cap")})
            continue

        try:
            kind, title, text = _extract_document(resp, timeout)
        except PdfToolMissing as e:
            attempts.append({"url": resp["url"], "ok": False,
                             "reason": str(e), "hint": POPPLER_HINT})
            continue
        except Exception as e:  # noqa: BLE001
            attempts.append({"url": resp["url"], "ok": False,
                             "reason": f"{type(e).__name__}: {e}"})
            continue

        # ar5iv 302s to the abstract page when it has no HTML rendition.
        if kind == "html" and re.search(r"arxiv\.org/abs/", resp["url"], re.I):
            attempts.append({"url": url, "ok": False, "reason": (
                f"redirected to the abstract page ({resp['url']}) — no HTML "
                "rendition exists for this paper")})
            continue
        if len(text) < MIN_USEFUL_CHARS:
            attempts.append({"url": resp["url"], "ok": False, "reason": (
                f"only {len(text)} characters of text — looks like a stub or "
                "error page, not the paper")})
            continue

        attempt = {"url": resp["url"], "ok": True}
        if note:
            attempt["note"] = note
        attempts.append(attempt)

        total = len(text)
        truncated = total > max_chars
        if truncated:
            text = text[:max_chars].rstrip() + (
                f"\n\n[truncated: {max_chars} of {total} characters shown — "
                "re-call fetch_paper with a larger max_chars for the rest]")
        return {
            "ok": True,
            "source_used": resp["url"],
            "content_type": kind,
            "title_guess": title or None,
            "text": text,
            "truncated": truncated,
            "chars": total,
            "attempts": attempts,
        }

    result = {
        "ok": False,
        "error": f"could not fetch {ref!r}: all {len(attempts)} source(s) failed",
        "attempts": attempts,
    }
    if any("pdftotext" in a.get("reason", "") for a in attempts):
        result["hint"] = POPPLER_HINT
    return result


# ------------------------------------------------- no-fabrication trace check

# Flag-only by design: an unmatched value is NOT proof of fabrication (it may
# be a derived quantity, a number quoted from cited work, or a hyperparameter
# recorded outside the evidence tree). It only means a human has to look at it.

EVIDENCE_EXTS = (".md", ".csv", ".json", ".txt")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv",
             ".mypy_cache", ".pytest_cache", "build", "dist"}
MAX_FILE_BYTES = 4 * 1024 * 1024

# Numbers, with thousands separators. The lookbehind keeps us out of
# identifiers (v2, fig3) and out of the middle of dotted runs (1.2.3).
NUMBER_RE = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)")

# Everything below is masked out of the .tex before numbers are extracted.
_TEX_MASKS = [
    re.compile(r"(?<!\\)%.*$", re.M),                                # comments
    re.compile(r"\\(?:cite[a-zA-Z]*|[a-zA-Z]*ref|label|input|include"
               r"(?:graphics)?|bibliography(?:style)?|addbibresource|url|href)"
               r"\s*(?:\[[^\]]*\])?\s*\{[^{}]*\}"),                  # keys/paths
    re.compile(r"\\begin\{tabular\*?\}\s*(?:\{[^{}]*\}|\[[^\]]*\])+"),  # col spec
    re.compile(r"\\(?:multicolumn|multirow)\s*\{[^{}]*\}"),
    re.compile(r"\\(?:hspace|vspace|hskip|vskip|setlength|addtolength|"
               r"scalebox|resizebox|arraystretch|columnsep)\s*\*?"
               r"\s*(?:\{[^{}]*\})*"),
    re.compile(r"\\(?:usepackage|documentclass)\s*(?:\[[^\]]*\])?\s*\{[^{}]*\}"),
    re.compile(r"(?i)\b(?:section|sec|subsection|subsubsection|figure|fig|"
               r"table|tab|appendix|algorithm|alg|equation|eq|listing|line|"
               r"step|phase|stage|definition|theorem|lemma|corollary|"
               r"proposition|chapter|part|item|footnote|column|row|level)s?"
               r"\.?~?\s*\d+(?:\.\d+)*[a-z]?\b"),                    # cross-refs
    re.compile(r"\b(?:1[89]|20)\d{2}\b(?!\s*(?:\\?%|x\b|\\times))"),  # years
    re.compile(r"\d+(?:\.\d+)?\s*(?:pt|pc|in|bp|cm|mm|dd|cc|sp|ex|em)\b"),
    re.compile(r"\d+(?:\.\d+)?\s*\\(?:text|line|column|page)width\b"),
    re.compile(r"\d+(?:\.\d+)?\s*\\(?:hsize|baselineskip|textheight)\b"),
    re.compile(r"[_^]\s*\{?\s*-?\s*\d+(?:\.\d+)?"),                  # sub/superscripts
]

# The leading [$}\\)]* skips whatever closes the math/macro the number sits in,
# so `$12.5$\%` and `\SI{12.5}{\percent}` are still recognized as percentages.
_TAIL_CLOSERS = r"[\s$}\\)]*?"
PERCENT_TAIL_RE = re.compile(r"^%s(?:\\?%%|\\?percent\b)" % _TAIL_CLOSERS)
MULTIPLIER_TAIL_RE = re.compile(
    r"^%s(?:\\times\b|[x\u00d7](?![\w.]))" % _TAIL_CLOSERS)


def _blank(match):
    """Replace a match with spaces, preserving length and line breaks."""
    return re.sub(r"[^\n]", " ", match.group(0))


def _mask_tex(text):
    for pattern in _TEX_MASKS:
        text = pattern.sub(_blank, text)
    return text


def _normalize_number(raw):
    """`1,234` → `1234`, `2.50` → `2.5`, `007` → `7`, `0.50` → `0.5`."""
    s = raw.replace(",", "").strip().lstrip("+")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
        if not s:
            return "0"
        whole, _, frac = s.partition(".")
        whole = str(int(whole or "0"))
        return f"{whole}.{frac}" if frac else whole
    return str(int(s or "0"))


def _classify(tail):
    if PERCENT_TAIL_RE.match(tail):
        return "percent"
    if MULTIPLIER_TAIL_RE.match(tail):
        return "multiplier"
    return "plain"


def _context(line):
    return re.sub(r"\s+", " ", line).strip()[:200]


def _extract_tex_values(text):
    """Yield {value, raw, kind, line, context} for each claimable number."""
    masked = _mask_tex(text)
    originals = text.split("\n")
    for lineno, line in enumerate(masked.split("\n"), 1):
        for m in NUMBER_RE.finditer(line):
            yield {
                "value": _normalize_number(m.group(1)),
                "raw": m.group(1),
                "kind": _classify(line[m.end():m.end() + 24]),
                "line": lineno,
                "context": _context(originals[lineno - 1]),
            }


class _EvidenceIndex:
    """Normalized numbers from the evidence tree, with rounding-tolerant lookup."""

    def __init__(self):
        self._exact = set()
        self._sorted = []

    def add_text(self, text):
        for m in NUMBER_RE.finditer(text):
            self._exact.add(_normalize_number(m.group(1)))

    def freeze(self):
        values = []
        for s in self._exact:
            try:
                values.append(float(s))
            except ValueError:  # pragma: no cover — normalization guarantees float
                pass
        self._sorted = sorted(values)
        return self

    def __len__(self):
        return len(self._exact)

    def _near(self, norm):
        """True if some evidence value rounds/truncates to `norm`."""
        try:
            value = float(norm)
        except ValueError:
            return False
        decimals = len(norm.partition(".")[2])
        tol = 0.5 * (10 ** -decimals) + 1e-9
        lo = bisect.bisect_left(self._sorted, value - tol)
        hi = bisect.bisect_right(self._sorted, value + tol)
        return hi > lo

    def matches(self, norm, kind="plain"):
        if norm in self._exact or self._near(norm):
            return True
        if kind == "percent":
            # A manuscript "95\%" is often stored as 0.95 in the evidence.
            try:
                value = float(norm)
            except ValueError:
                return False
            decimals = len(norm.partition(".")[2]) + 2
            fraction = _normalize_number(f"{value / 100:.{decimals}f}")
            return fraction in self._exact or self._near(fraction)
        return False


def _walk_files(root, exts):
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames
                             if d not in SKIP_DIRS and not d.startswith("."))
        for name in sorted(filenames):
            if name.lower().endswith(exts) and not name.startswith("."):
                found.append(os.path.join(dirpath, name))
    return found


def _read_capped(path):
    with open(path, errors="replace") as f:
        return f.read(MAX_FILE_BYTES)


def tool_trace_check(args):
    manuscript_dir = os.path.abspath(os.path.expanduser(args["manuscript_dir"]))
    if not os.path.isdir(manuscript_dir):
        return {"ok": False,
                "error": f"manuscript_dir not found: {manuscript_dir}"}

    evidence_paths = args.get("evidence_paths") or ["../experiments"]
    if isinstance(evidence_paths, str):
        evidence_paths = [evidence_paths]
    max_unmatched = max(1, min(int(args.get("max_unmatched", 200)), 2000))

    tex_files = _walk_files(manuscript_dir, (".tex",))
    if not tex_files:
        return {"ok": False,
                "error": f"no .tex files found under {manuscript_dir}"}

    warnings = []
    index = _EvidenceIndex()
    evidence_files = []
    for raw_path in evidence_paths:
        path = os.path.expanduser(str(raw_path))
        if not os.path.isabs(path):
            path = os.path.join(manuscript_dir, path)
        path = os.path.abspath(path)
        if os.path.isfile(path):
            evidence_files.append(path)
        elif os.path.isdir(path):
            evidence_files.extend(_walk_files(path, EVIDENCE_EXTS))
        else:
            warnings.append(f"evidence path not found: {path}")
    for path in evidence_files:
        try:
            index.add_text(_read_capped(path))
        except OSError as e:
            warnings.append(f"could not read {path}: {e}")
    index.freeze()
    if not evidence_files:
        warnings.append("no evidence files found — every value will be "
                        "reported as unmatched")

    total = 0
    unmatched = []
    seen = set()
    for tex in tex_files:
        try:
            source = _read_capped(tex)
        except OSError as e:
            warnings.append(f"could not read {tex}: {e}")
            continue
        rel = os.path.relpath(tex, manuscript_dir)
        for item in _extract_tex_values(source):
            key = (rel, item["line"], item["value"])
            if key in seen:
                continue
            seen.add(key)
            total += 1
            if index.matches(item["value"], item["kind"]):
                continue
            unmatched.append({
                "value": item["raw"],
                "normalized": item["value"],
                "kind": item["kind"],
                "file": rel,
                "line": item["line"],
                "context": item["context"],
            })

    unmatched.sort(key=lambda u: (u["file"], u["line"], u["normalized"]))
    result = {
        "ok": True,
        "total": total,
        "matched": total - len(unmatched),
        "unmatched_count": len(unmatched),
        "unmatched": unmatched[:max_unmatched],
        "scanned": {
            "tex_files": [os.path.relpath(p, manuscript_dir) for p in tex_files],
            "evidence_files": len(evidence_files),
            "evidence_values": len(index),
        },
        "note": ("Heuristic and flag-only: an unmatched value is NOT evidence "
                 "of fabrication (it may be derived, quoted from cited work, "
                 "or recorded outside the evidence tree) — but every unmatched "
                 "value should have been looked at by a human."),
    }
    if len(unmatched) > max_unmatched:
        result["truncated"] = True
    if warnings:
        result["warnings"] = warnings
    return result


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
    {
        "name": "fetch_paper",
        "description": (
            "Fetch a paper's full text as plain text. Give it an arXiv id/URL "
            "and it tries arxiv.org/html, then ar5iv (needed for anything "
            "submitted before ~Dec 2023), then the PDF; give it any other URL "
            "and it fetches directly, retrying with a browser User-Agent when "
            "the host blocks scripted access (usenix.org and friends). PDFs "
            "need `pdftotext` (poppler) on PATH. Returns source_used, "
            "title_guess, text, truncated — and, when everything fails, every "
            "source tried with the reason. Use this to actually read related "
            "work instead of relying on abstracts."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "ref": {"type": "string", "description": "arXiv id (2401.01234), arXiv/ar5iv URL, or any http(s) PDF/HTML URL"},
                "max_chars": {"type": "integer", "description": "Character budget for the returned text, 1000-400000; truncation is marked inline (default: 40000)"},
                "timeout": {"type": "integer", "description": "Seconds per source before giving up (default: 45)"},
            },
            "required": ["ref"],
        },
        "handler": tool_fetch_paper,
    },
    {
        "name": "trace_check",
        "description": (
            "Mechanical no-fabrication audit: extract every numeric claim from "
            "the manuscript's .tex sources (including inside math, percentages, "
            "N.Nx speedups, a--b ranges; skipping citation keys, cross-"
            "references, years, and layout dimensions) and check each one "
            "against the evidence files (.md/.csv/.json/.txt) under "
            "evidence_paths, allowing for rounded/truncated digits. Returns "
            "total, matched, and each unmatched value with file, line, and "
            "context. Heuristic and flag-only: unmatched does NOT mean "
            "fabricated (the value may be derived or quoted from cited work), "
            "but every unmatched value should have been looked at by a human."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "manuscript_dir": {"type": "string", "description": "Directory holding the .tex sources (scanned recursively)"},
                "evidence_paths": {"type": "array", "items": {"type": "string"}, "description": "Files or directories of evidence, relative to manuscript_dir or absolute (default: [\"../experiments\"])"},
                "max_unmatched": {"type": "integer", "description": "Cap on returned unmatched entries (default: 200)"},
            },
            "required": ["manuscript_dir"],
        },
        "handler": tool_trace_check,
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


# ---------------------------------------------------------------- self-test

def _self_test():
    """Offline unit tests for the parsing/matching helpers (no network).

    The two fetch_paper cases talk to a throwaway loopback HTTP server, so the
    whole suite still runs with the network unplugged.
    """
    import http.server
    import threading
    import unittest
    import unittest.mock

    class ArxivRefTests(unittest.TestCase):
        def test_recognizes_ids_and_urls(self):
            self.assertEqual(_arxiv_id("2401.01234"), "2401.01234")
            self.assertEqual(_arxiv_id("arXiv:1706.03762v5"), "1706.03762v5")
            self.assertEqual(_arxiv_id("https://arxiv.org/abs/1706.03762"),
                             "1706.03762")
            self.assertEqual(_arxiv_id("https://arxiv.org/pdf/2401.01234.pdf"),
                             "2401.01234")
            self.assertEqual(
                _arxiv_id("https://ar5iv.labs.arxiv.org/html/cs/0701001"),
                "cs/0701001")
            self.assertIsNone(_arxiv_id("https://www.usenix.org/paper.pdf"))
            self.assertIsNone(_arxiv_id("not a ref"))

        def test_mirror_order_is_html_ar5iv_pdf(self):
            html_url, ar5iv_url, pdf_url = _arxiv_sources("1706.03762")
            self.assertEqual(html_url, "https://arxiv.org/html/1706.03762")
            self.assertIn("ar5iv.labs.arxiv.org/html/1706.03762", ar5iv_url)
            self.assertEqual(pdf_url, "https://arxiv.org/pdf/1706.03762")

    class HtmlExtractionTests(unittest.TestCase):
        def test_structure_scripts_and_mathml(self):
            title, text = _html_to_text(
                "<html><head><title>Fast Widgets</title>"
                "<style>p{color:red}</style></head><body>"
                "<script>var x = 9999;</script>"
                "<h1>Fast Widgets</h1><p>We reduce latency.</p>"
                "<h2>2 Method</h2><p>The bound is "
                '<math alttext="\\alpha &lt; 3"><mi>a</mi></math> here.</p>'
                "</body></html>")
            self.assertEqual(title, "Fast Widgets")
            self.assertNotIn("9999", text)
            self.assertNotIn("color:red", text)
            self.assertIn("# Fast Widgets", text)
            self.assertIn("## 2 Method", text)
            self.assertIn("We reduce latency.", text)
            self.assertIn("$\\alpha < 3$", text)
            self.assertNotIn("<mi>", text)

    class NormalizationTests(unittest.TestCase):
        def test_normalize_number(self):
            self.assertEqual(_normalize_number("1,234"), "1234")
            self.assertEqual(_normalize_number("2.50"), "2.5")
            self.assertEqual(_normalize_number("2.0"), "2")
            self.assertEqual(_normalize_number("007"), "7")
            self.assertEqual(_normalize_number("0.50"), "0.5")
            self.assertEqual(_normalize_number("42"), "42")

    class TexExtractionTests(unittest.TestCase):
        def values(self, tex):
            return [v["value"] for v in _extract_tex_values(tex)]

        def test_extracts_math_percent_multiplier_and_ranges(self):
            tex = ("Throughput rose by $12.5$\\% and latency dropped "
                   "3.20x across 4--8 workers.\n")
            found = self.values(tex)
            self.assertEqual(found, ["12.5", "3.2", "4", "8"])
            kinds = {v["value"]: v["kind"] for v in _extract_tex_values(tex)}
            self.assertEqual(kinds["12.5"], "percent")
            self.assertEqual(kinds["3.2"], "multiplier")
            self.assertEqual(kinds["4"], "plain")

        def test_excludes_refs_years_specs_and_comments(self):
            tex = (
                "% we measured 777 times\n"
                "See Section 4.2 and Figure 3~\\cite{smith2019fast}.\n"
                "\\begin{tabular}{lcc}\n"
                "\\includegraphics[width=0.48\\textwidth]{fig1.pdf}\n"
                "\\vspace{12pt}\n"
                "Published in 2019, the baseline reaches $x_2$ ops.\n"
                "Our system reaches 63.5 ops.\n")
            found = self.values(tex)
            self.assertEqual(found, ["63.5"])

        def test_reports_file_line_and_context(self):
            tex = "intro\nWe observe a 91.4\\% hit rate.\n"
            item = list(_extract_tex_values(tex))[0]
            self.assertEqual(item["line"], 2)
            self.assertEqual(item["context"], "We observe a 91.4\\% hit rate.")

    class MatchingTests(unittest.TestCase):
        def index(self, text):
            idx = _EvidenceIndex()
            idx.add_text(text)
            return idx.freeze()

        def test_exact_match(self):
            idx = self.index("throughput,63.5\nworkers,8\n")
            self.assertTrue(idx.matches("63.5"))
            self.assertTrue(idx.matches("8"))
            self.assertFalse(idx.matches("999"))

        def test_rounding_tolerance_is_one_directional(self):
            idx = self.index('{"speedup": 3.417}')
            self.assertTrue(idx.matches("3.4"))    # manuscript rounded 3.417
            self.assertTrue(idx.matches("3.42"))   # ...to 2 decimals
            self.assertTrue(idx.matches("3"))
            self.assertFalse(idx.matches("3.45"))  # not a rounding of 3.417
            self.assertFalse(idx.matches("3.5"))
            # The other direction must not pass: a manuscript that is more
            # precise than the evidence cannot have been derived from it.
            coarse = self.index('{"speedup": 3.4}')
            self.assertFalse(coarse.matches("3.417"))
            self.assertFalse(coarse.matches("3.42"))

        def test_percent_matches_a_stored_fraction(self):
            idx = self.index('{"hit_rate": 0.95}')
            self.assertTrue(idx.matches("95", "percent"))
            self.assertFalse(idx.matches("95", "plain"))

    class TraceCheckToolTests(unittest.TestCase):
        def test_end_to_end(self):
            with tempfile.TemporaryDirectory() as root:
                manuscript = os.path.join(root, "paper")
                evidence = os.path.join(root, "experiments")
                os.makedirs(manuscript)
                os.makedirs(evidence)
                with open(os.path.join(manuscript, "main.tex"), "w") as f:
                    f.write("Ours reaches 63.5 ops, a 2.4x speedup over "
                            "the 41.9 baseline.\n")
                with open(os.path.join(evidence, "results.csv"), "w") as f:
                    f.write("system,ops\nours,63.5\nbaseline,26.4\n")

                out = tool_trace_check({"manuscript_dir": manuscript})
                self.assertTrue(out["ok"])
                self.assertEqual(out["total"], 3)
                self.assertEqual(out["matched"], 1)
                values = {u["value"] for u in out["unmatched"]}
                self.assertEqual(values, {"2.4", "41.9"})
                self.assertEqual(out["unmatched"][0]["file"], "main.tex")
                self.assertEqual(out["unmatched"][0]["line"], 1)
                self.assertIn("63.5", out["unmatched"][0]["context"])
                self.assertEqual(out["scanned"]["evidence_files"], 1)

        def test_error_paths(self):
            with tempfile.TemporaryDirectory() as root:
                missing = tool_trace_check(
                    {"manuscript_dir": os.path.join(root, "nope")})
                self.assertFalse(missing["ok"])
                self.assertIn("not found", missing["error"])

                empty = tool_trace_check({"manuscript_dir": root})
                self.assertFalse(empty["ok"])
                self.assertIn("no .tex files", empty["error"])

                os.makedirs(os.path.join(root, "paper"))
                with open(os.path.join(root, "paper", "m.tex"), "w") as f:
                    f.write("We hit 63.5 ops.\n")
                orphan = tool_trace_check(
                    {"manuscript_dir": os.path.join(root, "paper")})
                self.assertTrue(orphan["ok"])
                self.assertEqual(orphan["matched"], 0)
                self.assertTrue(any("not found" in w
                                    for w in orphan["warnings"]))

    class FetchPaperTests(unittest.TestCase):
        """fetch_paper against a loopback server that mimics a hostile publisher."""

        def serve(self, respond):
            outer = self

            class Handler(http.server.BaseHTTPRequestHandler):
                def do_GET(self):  # noqa: N802 — BaseHTTPRequestHandler API
                    respond(self, outer)

                def log_message(self, *_a):
                    pass

            try:
                srv = http.server.HTTPServer(("127.0.0.1", 0), Handler)
            except OSError as e:  # pragma: no cover — restricted sandboxes
                self.skipTest(f"cannot bind a loopback socket: {e}")
            threading.Thread(target=srv.serve_forever, daemon=True).start()
            self.addCleanup(srv.server_close)
            self.addCleanup(srv.shutdown)
            return "http://127.0.0.1:%d/paper" % srv.server_address[1]

        def test_browser_ua_retry_recovers_a_403(self):
            body = ("<html><head><title>Local Paper</title></head><body>"
                    "<h1>Local Paper</h1><p>"
                    + "We measured 42.5 ops per second. " * 40
                    + "</p></body></html>").encode()

            def respond(h, _t):
                # Exactly what usenix.org does to a non-browser User-Agent.
                if "Mozilla" not in h.headers.get("User-Agent", ""):
                    h.send_response(403)
                    h.end_headers()
                    h.wfile.write(b"forbidden")
                    return
                h.send_response(200)
                h.send_header("Content-Type", "text/html; charset=utf-8")
                h.send_header("Content-Length", str(len(body)))
                h.end_headers()
                h.wfile.write(body)

            out = tool_fetch_paper({"ref": self.serve(respond), "max_chars": 1000})
            self.assertTrue(out["ok"])
            self.assertEqual(out["title_guess"], "Local Paper")
            self.assertIn("browser User-Agent", out["attempts"][0]["note"])
            self.assertTrue(out["truncated"])
            self.assertEqual(out["chars"], 1334)
            self.assertIn("[truncated: 1000 of 1334 characters shown",
                          out["text"])
            self.assertIn("# Local Paper", out["text"])

        def test_pdf_without_poppler_reports_how_to_fix_it(self):
            pdf = b"%PDF-1.4\n% not a real pdf\n"

            def respond(h, _t):
                h.send_response(200)
                h.send_header("Content-Type", "application/pdf")
                h.send_header("Content-Length", str(len(pdf)))
                h.end_headers()
                h.wfile.write(pdf)

            url = self.serve(respond)
            with unittest.mock.patch.object(shutil, "which", return_value=None):
                out = tool_fetch_paper({"ref": url})
            self.assertFalse(out["ok"])
            self.assertIn("pdftotext", out["attempts"][0]["reason"])
            self.assertIn("poppler", out["attempts"][0]["hint"])
            self.assertIn("poppler", out["hint"])

    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite(
        loader.loadTestsFromTestCase(case) for case in (
            ArxivRefTests, HtmlExtractionTests, NormalizationTests,
            TexExtractionTests, MatchingTests, TraceCheckToolTests,
            FetchPaperTests))
    runner = unittest.TextTestRunner(verbosity=2)
    return 0 if runner.run(suite).wasSuccessful() else 1


def main():
    if "--self-test" in sys.argv[1:]:
        sys.exit(_self_test())
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
