$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot

$api = Start-Process powershell -PassThru -ArgumentList @(
  '-NoExit', '-Command',
  "Set-Location '$root\services\api'; uv run uvicorn app.main:app --reload --port 8000"
)

$web = Start-Process powershell -PassThru -ArgumentList @(
  '-NoExit', '-Command',
  "Set-Location '$root\apps\web'; npm run dev"
)

Write-Host "API process: $($api.Id)"
Write-Host "Web process: $($web.Id)"
Write-Host 'Open http://localhost:3000'
