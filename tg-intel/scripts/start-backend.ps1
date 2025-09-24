Param(
    [switch]$NoTee
)

$ErrorActionPreference = 'Stop'

# Always run from repo root (one level up from scripts)
$repoRoot = (Get-Item $PSScriptRoot).Parent.FullName
Set-Location -Path $repoRoot

# Force UTF-8 everywhere for reliable Unicode output on Windows
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONPATH = (Get-Location).Path
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)

# Resolve Python from venv if available (repo root .venv)
$python = Join-Path $repoRoot ".venv/ Scripts/ python.exe" -Resolve -ErrorAction SilentlyContinue
if (-not $python) { $python = Join-Path $repoRoot ".venv\Scripts\python.exe" }
if (-not (Test-Path $python)) { $python = 'python' }

# Start backend
if ($NoTee) {
  & $python -u .\start_backend.py
} else {
  & $python -u .\start_backend.py 2>&1 | Tee-Object -FilePath (Join-Path $repoRoot 'backend.log') -Encoding utf8
}


