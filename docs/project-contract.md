# Project contract

Complete this page at project setup. Use stable IDs for journeys and invariants so issues, tests and PRs can refer to them. The seed's initial contract covers its runnable CLI.

| Item | Current contract |
|---|---|
| Goal | Provide an installable Python starter with a runnable CLI |
| J1 | Clean install → run the CLI through its public entry point |
| I1 | The installed package exposes a working entry point |
| I2 | Core, persistence and UI obey the dependency rules in [architecture](architecture.md) |
| Scope | Local execution; record future external services and side effects here |
| Decisions | [ADRs](adr/) |
| Evidence | [Architecture tests](../tests/test_architecture.py) and the required CI check |

## Delivery protocol

1. Start from the current base commit. Read this contract, the issue and its latest evidence. State the affected journey, invariant and observable acceptance criterion before editing.
2. Identify callers, persisted data, configuration, provider contracts and operator instructions affected by the diff. Update the affected pieces together. Record deliberate scope changes in the issue or an ADR.
3. For a bug, demonstrate the regression on the old behavior and the corrected result on the new behavior when reproducible. Exercise the normal entry point. Record commands, results and evidence gaps. Keep offline fixtures, real provider runs and documentary evidence distinct.
4. Classify external writes, authentication, financial logic, migrations, and changes to CI or safeguards as critical. Require an independent reviewer to validate expected outcomes against the acceptance criteria and review failure modes appropriate to the change, including concurrency, restart and uncertain outcomes where applicable. Record review against the final head.
5. Before merging, verify the required checks on the final PR head. After merging, record the exact main SHA and its required checks before declaring the flow verified. Missing evidence leaves the criterion pending. Use a non-closing issue reference when verification must happen after merge.
6. For handoffs, record the base and current head, what was proved, what remains uncertain and the next concrete step in the issue or PR. Re-run the affected journey from a clean checkout when multiple PRs change it.

CI checks that the PR provides the required fields. Review determines whether the claims are true and the evidence is sufficient. Repository admins must enable and verify branch protection for the check to block merges.
