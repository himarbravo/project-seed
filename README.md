# My Project

Short project description.

> Status: early development (`0.x`). See [CHANGELOG.md](CHANGELOG.md).

<!-- seed:start -->
## How to use this template

This repository is a template: an empty Python project with the working protocol, the base documentation and CI already set up. The name `my-project` is a placeholder.

1. Create your repository from the template and clone it:
   ```bash
   gh repo create <user>/<name> --private --template himarbravo/project-seed --clone
   cd <name>
   ```
2. Rename the project. The script replaces the name in every file, renames the package, removes this section and deletes itself:
   ```bash
   python3 scripts/init_project.py <name> --owner <user> --author "<Your name>" \
       --description "<What the project does>"
   ```
3. Install, check and push the first commit:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -e ".[dev]"
   ./scripts/check.sh
   git add -A && git commit -m "chore: initialize project from seed" && git push
   ```
4. Configure the repository: create the labels [AGENTS.md](AGENTS.md) uses, allow squash merge only and protect `main`. It comes after the first push, because from then on nobody can push directly to `main`:
   ```bash
   ./scripts/setup_github.sh
   ```
5. Adapt what is specific to each project: [docs/architecture.md](docs/architecture.md), [docs/project-structure.md](docs/project-structure.md) and section 4 of [AGENTS.md](AGENTS.md).
<!-- seed:end -->

## Requirements

- Python 3.11 or later

## Development install

```bash
git clone https://github.com/OWNER/my-project.git
cd my-project
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

```bash
my-project              # or: python -m my_project
```

## Development

```bash
pytest                  # tests
ruff check .            # lint
ruff format .           # format
mypy                    # types
./scripts/check.sh      # all of the above, as in CI
```

## Documentation

| Document | Purpose |
|----------|---------|
| [AGENTS.md](AGENTS.md) | How we work: issues, branches, commits, PRs |
| [docs/project-structure.md](docs/project-structure.md) | Where everything is and where it goes |
| [docs/architecture.md](docs/architecture.md) | How it works inside |
| [docs/versioning.md](docs/versioning.md) | Versions and releases |
| [docs/adr/](docs/adr/) | Architecture decisions |

## License

[MIT](LICENSE). If the project needs another one, change `LICENSE` and the `license` field in `pyproject.toml`.
