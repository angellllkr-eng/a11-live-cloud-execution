# A11 local evaluator

Status: **PROVEN** for local evaluation. Status: **GATED** for Google Cloud AlphaEvolve.

## Run

From `A11-OWNER-RUNTIME`:

```powershell
.\SERVE.ps1
```

The service binds only to `127.0.0.1:8765`.

## Health

```powershell
Invoke-RestMethod http://127.0.0.1:8765/healthz
```

## Evaluate source

```powershell
$body = @{ code = (Get-Content .\path\to\program.py -Raw) } | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:8765/evaluate -Method Post -ContentType 'application/json' -Body $body
```

The candidate must define `evaluate(inputs)` and return a mapping containing the `sum_of_radii` metric. Candidate source is executed locally; do not expose this service to a network or production traffic.

## Benchmark

```powershell
.\BENCHMARK.ps1
```

The report is written to `BENCHMARK.json`.

This local path does not provide cloud Gemini generation, managed AlphaEvolve orchestration, distributed workers, or production serving. Those remain blocked until billing, ADC, the required API, and a verified Gemini Enterprise AlphaEvolve Engine/App ID are supplied and explicitly approved.
