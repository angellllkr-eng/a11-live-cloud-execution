# A11 OWNER RUNTIME - loopback-only evaluator
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root 'alphaevolve-on-googlecloud\.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $Python)) { throw 'BLOCKED: local AlphaEvolve venv missing' }
& $Python (Join-Path $PSScriptRoot 'serve_evaluator.py') --host 127.0.0.1 --port 8765 --concurrency 4
