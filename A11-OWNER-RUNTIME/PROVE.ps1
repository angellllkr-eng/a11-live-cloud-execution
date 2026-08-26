# A11 OWNER RUNTIME — Google Cloud CEO stack
# SAFE LOCAL. No billing, APIs, Terraform, Docker, or Cluster Toolkit.

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root 'alphaevolve-on-googlecloud\.venv\Scripts\python.exe'
$Proof = Join-Path $PSScriptRoot 'prove_seed.py'

if (-not (Test-Path -LiteralPath $Python)) {
  throw 'BLOCKED: local AlphaEvolve venv missing'
}
& $Python $Proof
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'PROVEN: A11 seed evaluator'
