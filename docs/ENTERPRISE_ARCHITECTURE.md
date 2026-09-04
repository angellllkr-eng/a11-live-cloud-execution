# A11-K Global Enterprise Architecture

## Authority

The **canonical enterprise architecture and repository registry live in `angellllkr-eng/agent-control-plane`**. This document is the execution-service view of that architecture.

Canonical control documents:
- `agent-control-plane/docs/ENTERPRISE_TREE_CANONICAL.md`
- `agent-control-plane/docs/REPOSITORY_REGISTRY.md`
- `agent-control-plane/ESTATE_MAP.md`

## Execution-service placement

```text
A11-K Global Enterprise
│
├── L0 — Governance & Authority
│   └── agent-control-plane
│
├── L1 — A11 Control Plane
│   ├── agent-control-plane
│   └── a11-live-cloud-execution  ← execution implementation
│
├── L2 — Security & Evidence
│   └── governed services / evidence controls
│
├── L3 — Cloud & Delivery Infrastructure
│   └── GitHub / CI / cloud deployment / state / automation
│
├── L4 — Digital Product Estate
│   └── MindReply / A11-K / AUREL / other approved products
│
├── L5 — External Systems & Trust Adapters
│
├── L6 — Physical Execution
│
└── L7 — Finance & Commercial Operations
```

## Local service architecture

```text
Operator / Product
       │
       ▼
A11 — governed reasoning + RAG orchestration
       │
       ├── multi-model routing
       ├── hybrid retrieval
       └── uncertainty / escalation
       │
       ▼
Halo — ingestion + pipeline automation
       │
       ├── deterministic chunking
       ├── embedding
       ├── namespace isolation
       └── provenance / evidence
       │
       ▼
Echo — governance + evidence
       │
       ├── hard constraints
       ├── append-only audit
       ├── signed evidence packages
       └── escalation
```

## Boundary rules

1. Models are execution resources; they never own policy or authority.
2. This repository implements services; it does not define the enterprise source of truth.
3. Owner approvals and production-control decisions belong to `agent-control-plane`.
4. Product/customer data belongs in the appropriate product root, not in private operational control storage.
5. Credentials never belong in repository content.
6. Production status requires current deployment, routing, health and smoke evidence.
7. Irreversible actions fail closed until the required approval is present.

## Execution contract

**Discover → Classify → Protect → Build → Validate → Approve (if required) → Deploy → Verify → Record → Monitor → Recover/Roll back.**

## Service readiness

This repository should be treated as an execution component until its deployment, API health, security controls, evidence flow and rollback path are independently verified. Documentation or repository presence alone does not establish `LIVE` status.
