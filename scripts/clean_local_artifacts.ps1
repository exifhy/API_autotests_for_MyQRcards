Write-Host "Cleaning Python and Allure local artifacts..." -ForegroundColor Cyan

Get-ChildItem -Path . -Recurse -Directory -Filter __pycache__ |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Get-ChildItem -Path . -Recurse -Include *.pyc,*.pyo -File |
    Remove-Item -Force -ErrorAction SilentlyContinue

if (Test-Path .\allure-results) {
    Remove-Item .\allure-results -Recurse -Force -ErrorAction SilentlyContinue
}

if (Test-Path .\allure-report) {
    Remove-Item .\allure-report -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "Local artifacts cleaned." -ForegroundColor Green
