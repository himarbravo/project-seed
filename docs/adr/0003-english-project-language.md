# 0003. English as the single project language

- **Status:** Accepted
- **Date:** 2026-10-29

## Context

The template wrote identifiers in English and docstrings, comments and documentation in Spanish. Projects created from it end up public or shared with people who do not read Spanish (for example, hackathon judges), and mixing two languages in one repository makes it harder to read and search. The template's owner asked on 2026-10-29 for everything in the template, and in the projects created from it, to be in English.

## Decision

Everything in the repository and on GitHub is written in English: code, docstrings, comments, documentation, ADRs, issues, pull requests, commit messages, CI messages and script output.

Accepted ADRs keep their rule of not being modified, with one exception: ADRs 0000 to 0002 are translated to English once, without changing their meaning. The translation is done in its own PR so the diff can be checked against the original.

## Alternatives considered

- **Keep Spanish for documentation:** no work, but every project created from the template starts half in Spanish.
- **Leave ADRs 0001 and 0002 in Spanish** as historical records: respects ADR immutability literally, but leaves Spanish text in a repository whose rule is now English only.

## Consequences

- AGENTS.md section 4 changes: identifiers, docstrings, comments and documentation are all in English.
- Commit summaries are written in English (AGENTS.md 2.3).
- Every project created from the template inherits this ADR.
- The remaining Spanish text is translated in a follow-up issue.
