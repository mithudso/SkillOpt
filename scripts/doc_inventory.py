"""Generate static source metadata without importing code or reading private state.

Run ``python scripts/doc_inventory.py`` after a source change. CI uses ``--check``.
The output is a navigation aid, not a semantic index or a coverage attestation.
"""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SUFFIXES = {".py", ".js", ".ts", ".sh", ".ps1", ".cmd", ".yml", ".yaml", ".toml", ".json", ".html", ".css"}
META_FILES = {".gitignore", ".editorconfig", ".gitattributes", ".env.example", "requirements.txt"}
EXCLUDED_PREFIXES = ("data/", "ckpt/", "skillopt-assets/", "skillopt/prompts/", "skillopt_sleep/prompts/")
EXCLUDED_FIXTURES = ("plugins/openclaw/tests/", "plugins/devin/fixtures/")
GENERATED = {
    "docs/high_signal_file_index.json", "docs/llm-repo-index.json",
    "docs/codebase-overview.md", "docs/tool-inventory.json",
    "docs/environment-variables.md", "docs/external-call-sites.json",
}
CALL_NAMES = {
    "subprocess.run", "subprocess.Popen", "subprocess.check_output", "subprocess.check_call",
    "urllib.request.urlopen", "requests.get", "requests.post", "urlopen",
}


def repository_paths(root: Path) -> list[str]:
    """Read indexed paths only; never admit another task's untracked files."""
    result = subprocess.run(
        ["git", "ls-files", "--cached", "-z"],
        cwd=root, check=True, capture_output=True,
    )
    paths = sorted(set(result.stdout.decode("utf-8").split("\0")) - {""})
    return [name for name in paths if name not in GENERATED and admitted(name)]


def admitted(name: str) -> bool:
    """Admit maintained code/configuration and prose, never frozen input bodies."""
    if name.endswith(".py") and name.startswith(("skillopt/prompts/", "skillopt_sleep/prompts/")):
        return True  # Runtime resource loaders are source, unlike prompt bodies.
    if name.startswith(EXCLUDED_PREFIXES + EXCLUDED_FIXTURES) or "/vendor/" in name:
        return False
    if name.startswith("skillopt/envs/") and name.endswith(".md"):
        return False  # Frozen benchmark prompts and seed skills.
    if name.startswith(("docs/code-deep-optimizer-", "docs/repo-bootstrap-audit-", "docs/maintenance-")):
        return False  # Run receipts index their source universe separately.
    path = Path(name)
    return path.suffix in SOURCE_SUFFIXES | {".md"} or name in META_FILES


def layer(name: str) -> str:
    if name.startswith("tests/"):
        return "test"
    if name.startswith("docs/") or name.endswith(".md"):
        return "docs"
    if name.startswith("skillopt_webui/"):
        return "frontend"
    if name.startswith(("scripts/", "plugins/")):
        return "tooling"
    if name.startswith(("skillopt/", "skillopt_sleep/")):
        return "library"
    return "config"


def python_metadata(name: str, source: str) -> tuple[dict[str, Any], list[dict], list[dict]]:
    """Parse source syntax only; never import an adapter, evaluator or provider."""
    tree = ast.parse(source, filename=name)
    summary = (ast.get_docstring(tree) or "").split("\n")[0]
    metadata: dict[str, Any] = {"exports": [], "depends_on": [], "summary": summary}
    metadata["exports"] = [
        node.name for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and not node.name.startswith("_")
    ]
    environment, calls = [], []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            metadata["depends_on"].extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            metadata["depends_on"].append("." * node.level + (node.module or ""))
        elif isinstance(node, ast.Call):
            function = ast.unparse(node.func)
            if function in {"os.getenv", "os.environ.get", "os.environ.setdefault"} and node.args:
                key = node.args[0]
                if isinstance(key, ast.Constant) and isinstance(key.value, str):
                    environment.append({"name": key.value, "path": name, "line": node.lineno})
            if function in CALL_NAMES or function.endswith((".chat.completions.create", ".responses.create")):
                calls.append({"path": name, "line": node.lineno, "call": function})
    metadata["depends_on"] = sorted(set(metadata["depends_on"]))
    return metadata, environment, calls


def collect(root: Path) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    cards, environment, calls, tools = [], [], [], []
    for name in repository_paths(root):
        path = root / name
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f"refusing source alias: {name}")
        if not path.is_file():
            continue  # A tracked file can be intentionally deleted before commit.
        card = {"path": name, "layer": layer(name), "exports": [], "depends_on": []}
        if path.suffix == ".py":
            source = path.read_text(encoding="utf-8")
            metadata, env, external = python_metadata(name, source)
            card.update(metadata)
            environment.extend(env)
            if not name.startswith("tests/"):
                calls.extend(external)
            if name.endswith("mcp_server.py"):
                for node in ast.parse(source).body:
                    if isinstance(node, ast.Assign) and any(
                        isinstance(target, ast.Name) and target.id == "TOOLS" for target in node.targets
                    ):
                        declared = ast.literal_eval(node.value)
                        tools.extend({"adapter": name, **tool} for tool in declared)
        summary = card.pop("summary", "")
        card["purpose"] = summary or f"{card['layer'].capitalize()} file: {Path(name).name}."
        card["provenance"] = "module docstring" if summary else "inferred from path and file type"
        cards.append(card)
    return cards, environment, calls, tools


def render(root: Path) -> dict[str, str]:
    cards, environment, calls, tools = collect(root)
    def encode(value: Any) -> str:
        return json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    outputs = {
        "docs/high_signal_file_index.json": encode(cards),
        "docs/llm-repo-index.json": encode({
            "schema": 1, "generator": "scripts/doc_inventory.py", "files": [row["path"] for row in cards],
            "exclusions": [*EXCLUDED_PREFIXES, *EXCLUDED_FIXTURES, "skillopt/envs/**/*.md", "**/vendor/", "generated indexes", "run receipts"],
        }),
        "docs/external-call-sites.json": encode({
            "generator": "scripts/doc_inventory.py", "scope": "static Python transport sites; aliases/dynamic calls need manual review",
            "calls": calls,
        }),
        "docs/tool-inventory.json": encode({"generator": "scripts/doc_inventory.py", "totalTools": len(tools), "tools": tools}),
    }
    overview = ["# Codebase file map", "", "Generated by `python scripts/doc_inventory.py`. Do not edit by hand.", "",
                "This static map lists maintained code, configuration and prose. It excludes frozen inputs, vendored code, generated indexes and dated run receipts. It reads Python syntax without importing code; inferred purposes are labeled in the JSON index.", ""]
    group = None
    for row in cards:
        directory = row["path"].split("/", 1)[0] if "/" in row["path"] else "Root"
        if directory != group:
            overview.extend([f"## {directory}", ""])
            group = directory
        overview.append(f"- `{row['path']}` — {row['purpose'].replace(chr(10), ' ')}")
    outputs["docs/codebase-overview.md"] = "\n".join(overview) + "\n"
    lines = ["# Environment variable names", "", "Generated from literal `os.getenv` and `os.environ` calls in maintained Python source. Values are never collected. Dynamic role-prefixed names and variables interpreted by external CLIs also exist; see [development](DEVELOPMENT.md).", "", "| Name | Static source |", "|---|---|"]
    by_name: dict[str, list[str]] = {}
    for row in environment:
        by_name.setdefault(row["name"], []).append(f"`{row['path']}:{row['line']}`")
    for name, sites in sorted(by_name.items()):
        lines.append(f"| `{name}` | {', '.join(sorted(set(sites)))} |")
    outputs["docs/environment-variables.md"] = "\n".join(lines) + "\n"
    return outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if static inventories drift")
    args = parser.parse_args(argv)
    outputs = render(ROOT)
    drift = []
    for name, expected in outputs.items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != expected:
                drift.append(name)
        else:
            path.write_text(expected, encoding="utf-8")
    if drift:
        print("Static documentation drift: " + ", ".join(drift))
        print("Regenerate with: python scripts/doc_inventory.py")
        return 1
    print(f"Static inventories {'checked' if args.check else 'written'}: {len(outputs)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
