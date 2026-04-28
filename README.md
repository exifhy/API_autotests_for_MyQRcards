# API Autotests — MyQRCards LK

API autotest framework for MyQRCards personal account (LK) backend.
Covers REST API endpoints: accounts, cards, companies, contacts, employees, subscriptions and more.

## Stack

- **Python 3.13** + **pytest**
- **Allure** for reports
- **Pydantic v2** for response validation
- **requests** for HTTP
- **GitHub Actions** for CI (scheduled runs on dev/prod)

## Coverage

- ~385 tests across 170+ test files
- `tests/api/` — unit-level API tests (per endpoint)
- `tests/e2e/` — end-to-end flow tests (create → verify → delete)
- Marks: `smoke`, `api`, `e2e`, `ng` (negative/auth)

## Project structure

```
services/        — API clients grouped by domain (accounts, cards, companies, ...)
src/             — helpers, models, fixtures, waiter utils
testkit/         — pytest fixtures
tests/api/       — per-endpoint API tests
tests/e2e/       — end-to-end flow tests
config/          — environment config, headers
data/            — ids templates (no secrets in repo)
```

## Architecture

All HTTP calls go through `Helper._call()` which automatically attaches to Allure:
- response time
- request URL + method
- response body

Services follow a single pattern:

```python
class SomeAPI(Helper):
    def get_something(self) -> SomeModel:
        response = self._call(
            "GET",
            url=self.endpoints.some_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK
        return SomeModel(**response.json())
```

## Setup (local)

**1. Clone and install dependencies:**

```bash
git clone https://github.com/exifhy/API_autotests_for_MyQRcards.git
cd API_autotests_for_MyQRcards
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
```

**2. Create env files (do NOT commit):**

```bash
copy .env.example .env.dev
copy .env.example .env.prod
```

Fill in `LK_JWT`, `APP_ID` and other variables.

**3. Create ids files (do NOT commit):**

```bash
copy data/ids.example.json data/ids.dev.json
copy data/ids.example.json data/ids.prod.json
```

Fill in `host`, `subscription_id`, `lk_account_id`, etc.

## Run

```bash
# All tests on dev
ENVIRON=dev .venv/Scripts/pytest tests/ --env=dev -v

# Smoke only
ENVIRON=dev .venv/Scripts/pytest tests/ --env=dev -m smoke -v

# E2E only
ENVIRON=dev .venv/Scripts/pytest tests/e2e/ --env=dev -v

# With Allure report
ENVIRON=dev .venv/Scripts/pytest tests/ --env=dev --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## CI — GitHub Actions

Scheduled runs via GitHub Actions:

| Schedule | Environment | Scope |
|---|---|---|
| Mon–Fri 10:00 | dev | all tests |
| Daily 02:00 | prod | smoke only |

Results are sent to Telegram after each run.
