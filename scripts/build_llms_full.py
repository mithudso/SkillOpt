"""Build /Users/mitch/dev/SkillOpt/llms-full.txt from key repo files.
Block grammar: '<!-- ===== file: PATH ===== -->' line, then '# PATH' (or '# PATH:A-B' for excerpts), blank line,
then the file text (markdown verbatim; code/config wrapped in a fenced block with a language tag)."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "llms-full.txt")

def MD(p):
    return (p, None, "md")
def SRC(p, lang, rng=None):
    return (p, rng, lang)

BLOCKS = [
 # -- docs (verbatim markdown)
 MD("README.md"),
 MD("docs/guide/installation.md"), MD("docs/guide/first-experiment.md"), MD("docs/guide/configuration.md"),
 MD("docs/guide/training-loop.md"), MD("docs/guide/skill-document.md"), MD("docs/guide/new-benchmark.md"),
 MD("docs/guide/new-backend.md"), MD("docs/guide/local-env-smoke.md"), MD("docs/guide/dl-analogy.md"),
 MD("docs/reference/cli.md"), MD("docs/reference/config.md"), MD("docs/reference/api.md"),
 MD("docs/sleep/README.md"), MD("docs/sleep/evalkit.md"), MD("docs/sleep/multi-skill-staging.md"),
 MD("docs/sleep/openai-compatible-endpoints.md"), MD("docs/sleep/RESULTS.md"),
 MD("plugins/README.md"), MD("plugins/claude-code/README.md"),

 MD("plugins/codex/README.md"), MD("plugins/cursor/README.md"), MD("plugins/copilot/README.md"),
 MD("plugins/devin/README.md"), MD("plugins/dsh/README.md"), MD("plugins/openclaw/README.md"),
 MD("data/README.md"), MD("ckpt/README.md"), MD("docs/contributing.md"), MD("CHANGELOG.md"),
 MD("skillopt/envs/_template/README.md"),
 # -- config files (fenced)
 SRC("pyproject.toml", "toml"), SRC(".env.example", "bash"),
 SRC("configs/_base_/default.yaml", "yaml"), SRC("configs/features/soft_gate.yaml", "yaml"),
 SRC("configs/searchqa/default.yaml", "yaml"), SRC("configs/docvqa/default.yaml", "yaml"),
 SRC("configs/alfworld/default.yaml", "yaml"), SRC("configs/officeqa/default.yaml", "yaml"),
 SRC("configs/livemathematicianbench/default.yaml", "yaml"), SRC("configs/spreadsheetbench/default.yaml", "yaml"),
 SRC("configs/skilltask/default.yaml", "yaml"),
 SRC("skillopt/envs/_template/config_template.yaml", "yaml"),
 # -- argparse / CLI sections
 SRC("scripts/train.py", "python", (130, 300)),
 SRC("scripts/train.py", "python", (371, 481)),
 SRC("scripts/train.py", "python", (641, 756)),
 SRC("scripts/eval_only.py", "python", (149, 244)),
 SRC("scripts/eval_only.py", "python", (559, 600)),
 SRC("scripts/materialize_searchqa.py", "python", (15, 34)),
 SRC("skillopt_sleep/__main__.py", "python", (97, 149)),
 SRC("skillopt_sleep/__main__.py", "python", (850, 897)),
 SRC("skillopt_webui/app.py", "python", (664, 684)),
 SRC("scripts/skillopt_skill.py", "python"),
 # -- config machinery and defaults
 SRC("skillopt/config.py", "python", (23, 272)),
 SRC("skillopt/model/common.py", "python", (18, 76)),
 SRC("skillopt/model/backend_config.py", "python", (139, 199)),
 SRC("skillopt_sleep/config.py", "python", (19, 93)),
 # -- extension surface
 SRC("skillopt/envs/base.py", "python"),
 SRC("skillopt/datasets/base.py", "python"),
 SRC("skillopt/envs/_template/env_template.py", "python"),
 SRC("skillopt/envs/_template/loader_template.py", "python"),
 SRC("skillopt/envs/skilltask/adapter.py", "python"),
 SRC("skillopt/envs/skilltask/dataloader.py", "python"),
 SRC("skillopt/envs/skilltask/rollout.py", "python"),
 SRC("skillopt/evaluation/gate.py", "python", (85, 225)),
 SRC("skillopt/optimizer/skill.py", "python", (85, 145)),
 SRC("skillopt_sleep/tasks_file.py", "python"),
 SRC("skillopt_sleep/judges.py", "python", (1, 40)),
 SRC("skillopt_sleep/memory.py", "python", (1, 56)),
 SRC("skillopt_sleep/types.py", "python", (48, 96)),
]

def read(p):
    return open(os.path.join(ROOT, p), encoding="utf-8").read()

def fence_for(text):
    n = 3
    while "`" * n in text:
        n += 1
    return "`" * n

def block(p, rng, lang):
    text = read(p)
    if lang == "md":
        label = p
        body = text.rstrip("\n") + "\n"
    else:
        lines = text.split("\n")
        if rng:
            a, b = rng
            body_text = "\n".join(lines[a-1:b])
            label = f"{p}:{a}-{b}"
        else:
            body_text = text.rstrip("\n")
            label = p
        f = fence_for(body_text)
        body = f"{f}{lang}\n{body_text}\n{f}\n"
    head = f"<!-- ===== file: {label} ===== -->\n# {label}\n\n"
    return label, head + body

parts, index = [], []
for p, rng, lang in BLOCKS:
    label, b = block(p, rng, lang)
    parts.append(b)
    index.append((label, len(b.encode())))

head = """# SkillOpt full reference (llms-full)

> Concatenated key documentation, CLI argument definitions, configs and extension code of the SkillOpt fork (package `skillopt` 0.2.0): everything needed to install it, train and evaluate skill documents, run SkillOpt-Sleep, and add an env.

<!-- generated 2026-10-05 by a build script from commit fa4ca18 plus fork-local working-tree files (scripts/skillopt_skill.py, skillopt/envs/skilltask/, configs/skilltask/); estimator: tokens = bytes / 4.
Grammar: every source file is one block. A block starts with the delimiter line `<!-- ===== file: LABEL ===== -->`, then the header line `# LABEL`, a blank line, then the content. LABEL is a repo-relative path, or `path:A-B` for an excerpt of lines A to B. Markdown sources are inserted verbatim (their own headings follow the block header); code and config sources are wrapped in a fenced block with a language tag so their `#` comments are not headings. Split on the delimiter line.
Prefer llms-small.txt for a cited how-to and llms-facts.txt for one-line facts; this file is the long form. -->

"""
toc = "<!-- blocks (label, bytes):\n" + "\n".join(f"  {lbl} {n}" for lbl, n in index) + "\n-->\n\n"
out = head + toc + "\n".join(parts)
open(OUT, "w", encoding="utf-8").write(out)
print(len(out.encode()), "bytes;", len(parts), "blocks")
