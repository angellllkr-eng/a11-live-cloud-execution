# A11 / MindReply cloud preflight — READ ONLY
$ErrorActionPreference = 'Continue'
$env:CLOUDSDK_METRICS_ENVIRONMENT = 'datacloud.ai-agent'
$Project = 'mind-reply-496111'
$Report = @{}

function Get-GcloudValue {
  param([string]$Cmd)
  $out = & cmd /c $Cmd 2>$null
  if ($LASTEXITCODE -eq 0 -and $out) { return ($out | Select-Object -First 1).Trim() }
  return $null
}

$Report.Project = $Project
$Report.Timestamp = (Get-Date).ToString('o')

$account = Get-GcloudValue "gcloud auth list --filter=status:ACTIVE --format=value(account)"
$Report.GCloudAccount = if ($account) { "PROVEN ($account)" } else { "BLOCKED" }

$projectState = Get-GcloudValue "gcloud projects describe $Project --format=value(lifecycleState)"
$Report.ProjectState = if ($projectState -eq 'ACTIVE') { "PROVEN (ACTIVE)" } else { "BLOCKED ($projectState)" }

$billing = Get-GcloudValue "gcloud billing projects describe $Project --format=value(billingEnabled)"
$Report.Billing = if ($billing -eq 'True') { "PROVEN" } else { "BLOCKED ($billing)" }

& gcloud auth application-default print-access-token --quiet 1>$null 2>$null
$Report.ADC = if ($LASTEXITCODE -eq 0) { "PROVEN" } else { "BLOCKED" }

$api = Get-GcloudValue "gcloud services list --enabled --project=$Project --filter=config.name=discoveryengine.googleapis.com --format=value(config.name)"
$Report.DiscoveryEngineAPI = if ($api) { "PROVEN" } else { "BLOCKED" }

$envFile = Join-Path $PSScriptRoot 'circle-packing.env'
$engineLine = Select-String -LiteralPath $envFile -Pattern '^GE_APP_ID=' -ErrorAction SilentlyContinue
$Report.GE_APP_ID = if ($engineLine -and $engineLine.Line -notmatch 'UNVERIFIED') { "PROVEN" } else { "UNVERIFIED" }

$Report.CloudMutation = "GATED"

$jsonPath = Join-Path $PSScriptRoot 'CLOUD-PREFLIGHT.json'
$Report | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

Write-Host "A11 CLOUD PREFLIGHT — report written to CLOUD-PREFLIGHT.json"
Write-Host ($Report | ConvertTo-Json -Depth 3)
