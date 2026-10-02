# X31 Architecture Contract

**Responsibility:** Cloud-native execution migration source

**Repository status:** LEGACY / SOURCE-FREEZE

## Domain boundary
Owns historical cloud-execution/governance/orchestration material for controlled extraction. It is not an independent production root.

## Typed agent/operator contract
Execution capabilities must be represented as explicit inputs, outputs, authorization requirements, and evidence expectations before migration. Current production authority remains outside this repository.

## Layer separation
Domain: historical cloud execution capabilities. Interface: migration-safe execution contracts. Shared: reusable schemas/utilities only. Tests: migration fixtures and contract tests; no claim of live deployment.

## Auditability
Migration provenance, destination, verification result, and retirement disposition must be recorded for promoted capabilities.

## Repository rule
This contract standardizes the repository boundary without creating a duplicate implementation. Existing capability is reconciled in place when this repository is canonical; legacy/source-freeze repositories remain provenance sources until reusable material is migrated and verified in its canonical destination.

## X31 invariant
**Domain → Agent/Operator Interface → Shared → Tests → Audit/Evidence**

No secret material belongs in Git. No production claim is valid without runtime evidence from the canonical deployment authority.
