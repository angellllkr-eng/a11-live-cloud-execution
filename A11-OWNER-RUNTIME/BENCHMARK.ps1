# A11 OWNER RUNTIME - local evaluator benchmark
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root 'alphaevolve-on-googlecloud\.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $Python)) { throw 'BLOCKED: local AlphaEvolve venv missing' }
& $Python (Join-Path $PSScriptRoot 'benchmark_local.py') --runs 1000
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
