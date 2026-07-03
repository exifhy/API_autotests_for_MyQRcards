param(
    [string]$EnvName = "dev",
    [string]$TestPath = "tests",
    [switch]$OpenReport
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$defaultPythonExe = Join-Path $repoRoot ".venv\Scripts\python.exe"
$pythonExe = if ($env:PYTHON_EXE) { $env:PYTHON_EXE } else { $defaultPythonExe }
$allureResults = Join-Path $repoRoot "allure-results"
$allureReport = Join-Path $repoRoot "allure-report"

if (-not (Test-Path $pythonExe)) {
    throw "Python executable not found: $pythonExe"
}

Write-Host "Cleaning Allure directories..." -ForegroundColor Cyan

if (Test-Path $allureResults) {
    Remove-Item $allureResults -Recurse -Force
}

if (Test-Path $allureReport) {
    Remove-Item $allureReport -Recurse -Force
}

New-Item -ItemType Directory -Path $allureResults | Out-Null

Write-Host "Running pytest for '$TestPath' on env '$EnvName'..." -ForegroundColor Cyan
$env:ENVIRON = $EnvName
& $pythonExe -m pytest -q $TestPath --env=$EnvName -p no:cacheprovider
if ($LASTEXITCODE -ne 0) {
    throw "Pytest finished with exit code $LASTEXITCODE"
}

Write-Host "Generating Allure report..." -ForegroundColor Cyan
& allure generate $allureResults --clean -o $allureReport
if ($LASTEXITCODE -ne 0) {
    throw "Allure generate finished with exit code $LASTEXITCODE"
}

Write-Host "Allure report is ready: $allureReport" -ForegroundColor Green

if ($OpenReport) {
    Write-Host "Opening Allure report..." -ForegroundColor Cyan
    & allure open $allureReport
    if ($LASTEXITCODE -ne 0) {
        throw "Allure open finished with exit code $LASTEXITCODE"
    }
}
