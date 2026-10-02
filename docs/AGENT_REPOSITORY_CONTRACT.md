# Agent Repository Contract — A11 Live Cloud Execution

**Status:** SOURCE-FREEZE / CAPABILITY MIGRATION
**Domain:** Historical cloud execution, governance, orchestration and evidence capabilities.
**Canonical product destination:** `Mind-Reply/mindreply-app`
**Boundary:** This repository is not an independent production root.

## Typed agent interface
Reusable execution capabilities must define typed command, authorization, result and evidence contracts before migration.

Recommended boundary:
- `domain/`: execution state machine and policy-independent business rules.
- `agent/`: operator command contract and adapters.
- `shared/`: typed execution/evidence schemas.
- `tests/`: unit, integration and execution simulation tests.

Do not copy code merely to satisfy directory naming; reconcile unique capability first.

## Auditability
Every execution command needs an actor/approval context, target, action, result and evidence reference.

## Verification
Destination behavior must be tested and evidenced before historical material is considered retired.
