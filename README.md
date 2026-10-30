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
   Details, manual steps and the private-repository limitation: [Protecting `main`](#protecting-main).
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

## Protecting `main`

`main` is protected so the rules in [AGENTS.md](AGENTS.md) enforce themselves: nobody, admins included, can push to it directly, force-push or delete it, and a pull request can only be merged when CI is green.

### With the script (recommended)

Run it once, after the first push to `main` (afterwards nobody can push there directly). It needs the [GitHub CLI](https://cli.github.com/) logged in as an account with admin rights on the repository. It changes repository settings, so a person runs it, not an agent.

```bash
gh auth status              # check you are logged in as the repository admin
./scripts/setup_github.sh
```

It configures:

| Setting | Value |
|---------|-------|
| Labels | `type:feature`, `type:bug`, `type:refactor`, `type:docs`, `type:chore` |
| Merge methods | Squash only; merge commits and rebase merging are turned off |
| Branches | Deleted automatically after merging |
| `main` | Pull request required (0 approvals, so it works for one person); `required` and `conventions` checks must pass on an up-to-date branch; linear history; no force pushes or deletions; applies to admins too |

It is safe to run again: labels are updated in place and the settings are simply reapplied.

Check that it worked:

```bash
gh api repos/{owner}/{repo}/branches/main --jq .protected     # prints true
```

A direct `git push origin main` is now rejected.

### By hand, in the GitHub web interface

If you cannot use the script, the same settings are in the repository's **Settings**:

1. **General → Pull Requests:** untick *Allow merge commits* and *Allow rebase merging*, keep *Allow squash merging*, and tick *Automatically delete head branches*.
2. **Branches → Add classic branch protection rule**, with *Branch name pattern* `main`:
   - Tick *Require a pull request before merging*, and leave *Require approvals* unticked if you work alone.
   - Tick *Require status checks to pass before merging* and *Require branches to be up to date before merging*, then add the `required` and `conventions` checks. They only appear in the search box after they have run once, so open a first pull request before this step.
   - Tick *Require linear history* and *Do not allow bypassing the above settings*.
   - Leave *Allow force pushes* and *Allow deletions* unticked.
   - Click **Create**.
3. **Issues → Labels:** create the five `type:` labels listed above.

### Private repositories

GitHub only offers branch protection on private repositories with a paid plan (GitHub Pro, Team or Enterprise); on GitHub Free it is available for public repositories only ([GitHub docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)). On a private repository with GitHub Free the script stops with an error at that step, after the labels and merge settings are already applied. Until the repository is public or on a paid plan, the protection depends on everyone following AGENTS.md.

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
