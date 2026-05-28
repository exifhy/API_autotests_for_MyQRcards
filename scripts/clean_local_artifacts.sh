#!/usr/bin/env bash

set -euo pipefail

echo "Cleaning Python and Allure local artifacts..."

find . -type d -name "__pycache__" -prune -exec rm -rf {} +
find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete

rm -rf ./allure-results ./allure-report

echo "Local artifacts cleaned."
