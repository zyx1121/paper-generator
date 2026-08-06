#!/usr/bin/env python3
"""Repository consistency checks for the paper-generator plugin.

Stdlib only, Python 3.11+. Run the whole suite locally exactly as CI does:

    python3 scripts/ci_checks.py

Optional: run a subset with ``--only links,plugin`` (names printed in the
summary). ``--list`` prints the available check names.

Design rule for the fuzzy checks (cross-refs, anchors): prefer a miss over a
false alarm. A red CI on a prose heuristic is worse than an unreported typo.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

REPO_ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {".git", ".github", "__pycache__", "node_modules", ".venv", "venv"}

# Schemes that are never repo-relative paths.
EXTERNAL_SCHEME = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.IGNORECASE)

# [text](target) — target stops at the first whitespace so `(path "title")`
# degrades gracefully. Angle-bracket targets are unwrapped below.
MD_LINK = re.compile(r"\[(?P<text>(?:[^\[\]]|\[[^\[\]]*\])*)\]\((?P<target>[^)\s]*)")

HEADING = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+?)\s*#*\s*$", re.MULTILINE)

# A section cross-reference: "§Pipeline acknowledgement", "§2b", "§4.1".
SECTION_REF = re.compile(r"§\s*(?P<label>[0-9]+[a-z]?(?:\.[0-9]+)*|[A-Z][A-Za-z]*(?:\s+[a-z][A-Za-z-]*){0,4})")

FENCE = re.compile(r"^\s*(?:```|~~~)")

SEMVER = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+(?P<build>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)

PLUGIN_MANIFEST = Path(".claude-plugin/plugin.json")
MCP_SERVER = Path("mcp/paper_tools.py")


@dataclass
class Result:
    """Outcome of one check: hard errors fail CI, warnings only inform."""

    name: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checked: int = 0
    detail: str = ""

    @property
    def ok(self) -> bool:
        return not self.errors


# --------------------------------------------------------------------------
# shared helpers
# --------------------------------------------------------------------------


def markdown_files() -> list[Path]:
    out: list[Path] = []
    for path in sorted(REPO_ROOT.rglob("*.md")):
        rel = path.relative_to(REPO_ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        out.append(path)
    return out


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def strip_code_spans(text: str) -> str:
    """Blank out fenced blocks and inline code, keeping byte offsets stable."""
    out = list(text)
    lines = text.split("\n")
    offset = 0
    in_fence = False
    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
            for i in range(offset, offset + len(line)):
                out[i] = " "
        elif in_fence:
            for i in range(offset, offset + len(line)):
                out[i] = " "
        offset += len(line) + 1

    blanked = "".join(out)
    result = list(blanked)
    for match in re.finditer(r"`+[^`\n]*`+", blanked):
        for i in range(match.start(), match.end()):
            result[i] = " "
    return "".join(result)


def headings(text: str) -> list[str]:
    return [m.group("title").strip() for m in HEADING.finditer(text)]


def slugify(title: str) -> str:
    """GitHub-ish anchor slug (lowercase, punctuation dropped, spaces to -)."""
    title = unicodedata.normalize("NFKD", title)
    title = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", title)  # links -> text
    title = title.replace("`", "").replace("*", "").replace("_", "")
    title = title.lower()
    title = re.sub(r"[^\w\s-]", "", title)
    return re.sub(r"\s+", "-", title.strip())


def normalize(text: str) -> str:
    """Loose comparison form: lowercase alphanumerics and single spaces."""
    text = unicodedata.normalize("NFKD", text).lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return text.strip()


# --------------------------------------------------------------------------
# 1. internal markdown links
# --------------------------------------------------------------------------


def check_links() -> Result:
    result = Result("links", detail="relative [text](path) targets in *.md")
    for path in markdown_files():
        text = strip_code_spans(read(path))
        for match in MD_LINK.finditer(text):
            raw = match.group("target").strip()
            if raw.startswith("<") and raw.endswith(">"):
                raw = raw[1:-1]
            if not raw or EXTERNAL_SCHEME.match(raw):
                continue  # http(s), mailto:, protocol-relative — not ours to verify

            target, _, anchor = raw.partition("#")
            location = f"{rel(path)}:{line_of(text, match.start())}"

            if not target:
                # Pure in-page anchor.
                _check_anchor(result, path, read(path), anchor, raw, location)
                continue

            result.checked += 1
            resolved = _resolve(path.parent, target)
            if resolved is None or not resolved.exists():
                result.errors.append(f"{location}: link target not found: {raw}")
                continue
            if anchor and resolved.is_file() and resolved.suffix == ".md":
                _check_anchor(result, resolved, read(resolved), anchor, raw, location)
    return result


def _resolve(base_dir: Path, target: str) -> Path | None:
    """Resolve a repo-relative link target, or None if it escapes the repo."""
    target = unquote(target)
    if target.startswith("/"):
        candidate = REPO_ROOT / target.lstrip("/")
    else:
        candidate = base_dir / target
    try:
        candidate = candidate.resolve()
    except OSError:
        return None
    if REPO_ROOT not in candidate.parents and candidate != REPO_ROOT:
        return None  # points outside the repo; not our business
    return candidate


def _check_anchor(result: Result, path: Path, text: str, anchor: str, raw: str, location: str) -> None:
    """Anchors are a warning-only check: slug rules vary between renderers."""
    if not anchor:
        return
    slugs = {slugify(title) for title in headings(text)}
    if not slugs:
        return
    want = slugify(anchor)
    if want in slugs:
        return
    if any(slug.startswith(want) or want in slug for slug in slugs):
        return
    result.warnings.append(f"{location}: anchor may not exist: {raw}")


# --------------------------------------------------------------------------
# 2. cross-references of the form "<skill or file> §<section>"
# --------------------------------------------------------------------------


def skill_files() -> dict[str, Path]:
    out: dict[str, Path] = {}
    skills_dir = REPO_ROOT / "skills"
    if not skills_dir.is_dir():
        return out
    for entry in sorted(skills_dir.iterdir()):
        skill = entry / "SKILL.md"
        if skill.is_file():
            out[entry.name.lower()] = skill
    return out


def check_crossrefs() -> Result:
    """Heuristic: only verify a §ref when the nearby prose names a real file.

    Bare "(§3)" style references point at the *paper being written*, not at a
    document in this repo, so they are skipped by construction.
    """
    result = Result("crossrefs", detail="'<skill|file>.md §Section' references")
    skills = skill_files()
    md_by_name: dict[str, list[Path]] = {}
    for path in markdown_files():
        md_by_name.setdefault(path.name.lower(), []).append(path)

    for path in markdown_files():
        text = strip_code_spans(read(path))
        for match in SECTION_REF.finditer(text):
            label = match.group("label").strip()
            window = text[max(0, match.start() - 160) : match.start()]
            window = re.sub(r"\s+", " ", window)
            numeric = bool(re.match(r"^[0-9]", label))

            target = _crossref_target(window, path, skills, md_by_name, numeric)
            if target is None or target == path:
                continue

            result.checked += 1
            titles = headings(read(target))
            if not titles:
                continue
            if not _heading_matches(label, titles):
                location = f"{rel(path)}:{line_of(text, match.start())}"
                result.errors.append(
                    f"{location}: §{label} not found as a heading in {rel(target)}"
                )
    return result


def _crossref_target(
    window: str,
    source: Path,
    skills: dict[str, Path],
    md_by_name: dict[str, list[Path]],
    numeric: bool,
) -> Path | None:
    """Closest preceding file mention wins; None means 'not confident, skip'."""
    candidates: list[tuple[int, Path]] = []

    for match in re.finditer(r"([A-Za-z0-9_.-]+\.md)", window):
        name = match.group(1).lower()
        sibling = source.parent / match.group(1)
        if sibling.is_file():
            candidates.append((match.start(), sibling))
        elif len(md_by_name.get(name, [])) == 1:
            candidates.append((match.start(), md_by_name[name][0]))

    for match in re.finditer(r"\b([A-Za-z][A-Za-z-]*)\s+(?:SKILL|skill)\b", window):
        skill = skills.get(match.group(1).lower())
        if skill is not None:
            candidates.append((match.start(), skill))

    if not numeric:
        # A textual label ("§Pipeline acknowledgement") is specific enough that
        # a bare skill name nearby is a safe anchor. Numeric labels are not.
        for match in re.finditer(r"\b([A-Za-z][A-Za-z-]*)\b", window):
            skill = skills.get(match.group(1).lower())
            if skill is not None:
                candidates.append((match.start(), skill))

    if not candidates:
        return None
    return max(candidates, key=lambda item: item[0])[1]


def _heading_matches(label: str, titles: list[str]) -> bool:
    want = normalize(label)
    if not want:
        return True
    for title in titles:
        got = normalize(title)
        if not got:
            continue
        if got == want or got.startswith(want + " ") or got.startswith(want):
            return True
        if want in got:
            return True
        # "2b" vs "### 2b. Field-specific sources"
        if re.match(rf"^{re.escape(want)}\b", got):
            return True
    return False


# --------------------------------------------------------------------------
# 3. plugin manifest
# --------------------------------------------------------------------------


def check_plugin_json() -> Result:
    result = Result("plugin", detail=f"{PLUGIN_MANIFEST} shape and version")
    path = REPO_ROOT / PLUGIN_MANIFEST
    if not path.is_file():
        result.errors.append(f"{PLUGIN_MANIFEST}: file not found")
        return result

    result.checked += 1
    try:
        data = json.loads(read(path))
    except json.JSONDecodeError as exc:
        result.errors.append(f"{PLUGIN_MANIFEST}: invalid JSON: {exc}")
        return result

    if not isinstance(data, dict):
        result.errors.append(f"{PLUGIN_MANIFEST}: top level must be an object")
        return result

    for key in ("name", "version", "description"):
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            result.errors.append(f"{PLUGIN_MANIFEST}: missing or empty required field '{key}'")

    version = data.get("version")
    if isinstance(version, str) and not SEMVER.match(version.strip()):
        result.errors.append(f"{PLUGIN_MANIFEST}: version '{version}' is not SemVer (MAJOR.MINOR.PATCH)")

    mcp = data.get("mcpServers")
    if isinstance(mcp, str):
        # Manifest paths are relative to the plugin root, not to the manifest.
        referenced = _resolve(REPO_ROOT, mcp)
        if referenced is None or not referenced.exists():
            result.errors.append(f"{PLUGIN_MANIFEST}: mcpServers path not found: {mcp}")

    return result


# --------------------------------------------------------------------------
# 4. SKILL.md frontmatter
# --------------------------------------------------------------------------


def check_frontmatter() -> Result:
    result = Result("frontmatter", detail="skills/*/SKILL.md YAML frontmatter")
    skills = skill_files()
    if not skills:
        result.errors.append("skills/: no skills/*/SKILL.md found")
        return result

    for name, path in skills.items():
        result.checked += 1
        fields = _frontmatter(read(path))
        if fields is None:
            result.errors.append(f"{rel(path)}: missing '---' YAML frontmatter block")
            continue
        for key in ("name", "description"):
            if not fields.get(key):
                result.errors.append(f"{rel(path)}: frontmatter missing or empty '{key}'")
        declared = fields.get("name", "")
        if declared and declared.lower() != name:
            result.errors.append(
                f"{rel(path)}: frontmatter name '{declared}' does not match directory '{name}'"
            )
    return result


def _frontmatter(text: str) -> dict[str, str] | None:
    """Minimal YAML: top-level `key: value`, plus folded (`>`/`|`) blocks."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None

    fields: dict[str, str] = {}
    key: str | None = None
    for line in lines[1:end]:
        match = re.match(r"^(?P<key>[A-Za-z_][\w-]*)\s*:\s*(?P<value>.*)$", line)
        if match:
            key = match.group("key")
            value = match.group("value").strip()
            fields[key] = "" if value in (">", "|", ">-", "|-", "") else value.strip("\"'")
        elif key and line.strip() and line.startswith((" ", "\t")):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


# --------------------------------------------------------------------------
# 5. python syntax
# --------------------------------------------------------------------------


def check_python() -> Result:
    result = Result("python", detail="py_compile over tracked *.py")
    targets = [REPO_ROOT / MCP_SERVER]
    for path in sorted(REPO_ROOT.rglob("*.py")):
        r = path.relative_to(REPO_ROOT)
        if any(part in SKIP_DIRS for part in r.parts):
            continue
        if path not in targets:
            targets.append(path)

    # Keep generated .pyc out of the working tree.
    env = dict(os.environ)
    with tempfile.TemporaryDirectory(prefix="ci-pycache-") as cache:
        env["PYTHONPYCACHEPREFIX"] = cache
        for path in targets:
            if not path.is_file():
                result.errors.append(f"{rel(path)}: file not found")
                continue
            result.checked += 1
            proc = subprocess.run(
                [sys.executable, "-m", "py_compile", str(path)],
                capture_output=True,
                text=True,
                env=env,
            )
            if proc.returncode != 0:
                detail = (proc.stderr or proc.stdout).strip().splitlines()
                tail = detail[-1] if detail else f"exit {proc.returncode}"
                result.errors.append(f"{rel(path)}: py_compile failed: {tail}")
    return result


# --------------------------------------------------------------------------
# 6. MCP server self-test
# --------------------------------------------------------------------------


def check_selftest() -> Result:
    result = Result("selftest", detail=f"{MCP_SERVER} --self-test (offline unit tests)")
    server = REPO_ROOT / MCP_SERVER
    if not server.is_file():
        result.errors.append(f"{MCP_SERVER}: file not found")
        return result
    result.checked = 1
    proc = subprocess.run(
        [sys.executable, str(server), "--self-test"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip().splitlines()
        tail = detail[-1] if detail else f"exit {proc.returncode}"
        result.errors.append(f"{MCP_SERVER}: self-test failed: {tail}")
    return result


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------

CHECKS = {
    "links": check_links,
    "crossrefs": check_crossrefs,
    "plugin": check_plugin_json,
    "frontmatter": check_frontmatter,
    "python": check_python,
    "selftest": check_selftest,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", help="comma-separated subset of checks to run")
    parser.add_argument("--list", action="store_true", help="list check names and exit")
    args = parser.parse_args(argv)

    if args.list:
        for name in CHECKS:
            print(name)
        return 0

    selected = list(CHECKS)
    if args.only:
        selected = [name.strip() for name in args.only.split(",") if name.strip()]
        unknown = [name for name in selected if name not in CHECKS]
        if unknown:
            parser.error(f"unknown check(s): {', '.join(unknown)}")

    failed = 0
    warned = 0
    for name in selected:
        result = CHECKS[name]()
        status = "PASS" if result.ok else "FAIL"
        print(f"[{status}] {result.name:<12} {result.checked:>3} checked — {result.detail}")
        for message in result.warnings:
            print(f"         warn: {message}")
        for message in result.errors:
            print(f"         error: {message}")
        failed += 0 if result.ok else 1
        warned += len(result.warnings)

    print()
    if failed:
        print(f"FAILED: {failed} of {len(selected)} check(s) reported errors")
        return 1
    print(f"OK: {len(selected)} check(s) passed" + (f", {warned} warning(s)" if warned else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
