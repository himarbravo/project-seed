"""Turns the template into a project with its own name.

Replaces the placeholder name `my-project` in every file, renames the
`src/my_project/` package, removes the template usage section from the README,
deletes the workflow that tests the template and deletes itself.

Usage (from the repository root, once):

    python3 scripts/init_project.py my-app --owner username --author "Name" \
        --description "What the project does"
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".ruff_cache"}
SEED_SECTION = re.compile(r"<!-- seed:start -->.*?<!-- seed:end -->\n\n?", re.DOTALL)


def text_files() -> list[Path]:
    this_script = Path(__file__).resolve()
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path == this_script:
            continue
        if SKIP_DIRS & set(path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialises a project from the template.")
    parser.add_argument("name", help="project name in kebab-case, e.g. my-app")
    parser.add_argument("--owner", help="GitHub user or organisation")
    parser.add_argument("--author", help="author shown in pyproject.toml")
    parser.add_argument("--description", help="short project description")
    args = parser.parse_args()

    if not re.fullmatch(r"[a-z][a-z0-9]*(-[a-z0-9]+)*", args.name):
        sys.exit("The name must be kebab-case: lowercase letters, digits and hyphens.")
    if not (ROOT / "src" / "my_project").is_dir():
        sys.exit("src/my_project/ does not exist: this project is already initialised.")

    package = args.name.replace("-", "_")
    year = date.today().year
    replacements = {
        "(c) YEAR": f"(c) {year}",
        "my-project": args.name,
        "my_project": package,
        "My Project": args.name.replace("-", " ").title(),
    }
    if args.owner:
        replacements["github.com/OWNER/"] = f"github.com/{args.owner}/"
    if args.author:
        replacements['name = "AUTHOR"'] = f'name = "{args.author}"'
        replacements[f"(c) {year} AUTHOR"] = f"(c) {year} {args.author}"
    if args.description:
        replacements["Descripción corta del proyecto."] = args.description

    for path in text_files():
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        text = original
        if path == ROOT / "README.md":
            text = SEED_SECTION.sub("", text)
        for old, new in replacements.items():
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")

    (ROOT / "src" / "my_project").rename(ROOT / "src" / package)
    (ROOT / ".github" / "workflows" / "seed.yml").unlink(missing_ok=True)
    Path(__file__).unlink()
    print(f"Project initialised as {args.name} (package {package}).")


if __name__ == "__main__":
    main()
