# A11 OWNER RUNTIME — AGENT CONTRACT

Owner: София Tech Register EOOD  
Brand: A11 / MindReply  
Portfolio: A11-K.space

## Absolute rule

**NEVER GET STUCK.**

If Plan A fails → execute Plan B immediately.  
If Plan B fails → Plan C.  
Continue through **A → Z**.  
**Q is always the emergency backup lane.**

Config source of truth:

* `AGENT-ROUTES-A-TO-Z.json`

## Status vocabulary only

* PROVEN
* READY
* BLOCKED
* FAILED
* UNVERIFIED
* GATED

## Every agent must

1. Read `AGENT-ROUTES-A-TO-Z.json` first.
2. Choose the strongest available local route.
3. On any failure, jump to `on_fail` with no waiting.
4. If uncertain, use **Q**.
5. Keep cloud mutations GATED until owner unlock.
6. Never invent success.
7. Never expose secrets, keys, tokens, or `.env` secrets.
8. Prefer loopback-only services.
9. Write evidence artifacts for every material result.
10. Keep working for the owner with alternatives until A→Z is exhausted.

## Live surfaces

| Surface | URL | Status |
|---|---|---|
| Evaluator | http://127.0.0.1:8765 | READY |
| Live monitor | http://127.0.0.1:8766 | PROVEN |

## Model selector (UI labels)

* Gemini 3.7 → remote GATED
* Grok 6 → remote GATED
* Sol 5.6 → remote GATED
* NVIDIA Pro tier → remote GATED

Local sample analysis is allowed. Remote inference is not enabled.

## Fast path

```powershell
cd C:\Users\ANGEL\OneDrive\Desktop\google-cloud-ceo-stack-2026-08-23
.\A11-OWNER-RUNTIME\PROVE.ps1
.\A11-OWNER-RUNTIME\BENCHMARK.ps1
.\A11-OWNER-RUNTIME\MONITOR.ps1
.\A11-OWNER-RUNTIME\CLOUD-PREFLIGHT.ps1
```

## Owner gates only

* billing attach
* `gcloud auth application-default login`
* real `GE_APP_ID`
* API enablement
* deploy / IAM / DNS / public bind
