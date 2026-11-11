$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot

Write-Host 'Setting up FastAPI backend...'
Push-Location "$root\services\api"
uv sync
Pop-Location

Write-Host 'Setting up Next.js frontend...'
Push-Location "$root\apps\web"
npm install
Pop-Location

Write-Host ''
Write-Host 'Setup complete.' -ForegroundColor Green
Write-Host 'Run .\scripts\dev.ps1 from the project root.'
