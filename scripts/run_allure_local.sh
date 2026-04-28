#!/usr/bin/env bash

set -euo pipefail

ENV_NAME="dev"
TEST_PATH="tests"
OPEN_REPORT="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env)
      ENV_NAME="$2"
      shift 2
      ;;
    --tests)
      TEST_PATH="$2"
      shift 2
      ;;
    --open)
      OPEN_REPORT="true"
      shift
      ;;
    *)
      echo "Unknown argument: $1"
      echo "Usage: ./scripts/run_allure_local.sh [--env dev|prod] [--tests path] [--open]"
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_EXE="${PYTHON_EXE:-$REPO_ROOT/.venv/Scripts/python.exe}"
ALLURE_RESULTS="$REPO_ROOT/allure-results"
ALLURE_REPORT="$REPO_ROOT/allure-report"

if [[ ! -f "$PYTHON_EXE" ]]; then
  echo "Python executable not found: $PYTHON_EXE"
  exit 1
fi

echo "Cleaning Allure directories..."
rm -rf "$ALLURE_RESULTS" "$ALLURE_REPORT"
mkdir -p "$ALLURE_RESULTS"

echo "Running pytest for '$TEST_PATH' on env '$ENV_NAME'..."
ENVIRON="$ENV_NAME" "$PYTHON_EXE" -m pytest -q "$TEST_PATH" --env="$ENV_NAME" -p no:cacheprovider

echo "Generating Allure report..."
allure generate "$ALLURE_RESULTS" --clean -o "$ALLURE_REPORT"

echo "Allure report is ready: $ALLURE_REPORT"

if [[ "$OPEN_REPORT" == "true" ]]; then
  echo "Opening Allure report..."
  allure open "$ALLURE_REPORT"
fi
