"""
Script-run stability tests.

Run N times to verify the flow is stable:
    pytest tests/e2e/test_script_runs.py --runs=5 --env=dev -v

These tests are intentionally excluded from CI (no smoke/regress marks).
"""
from http import HTTPStatus

import allure
import pytest
from loguru import logger

from services.companies.company_create.payloads import Payloads as CompanyPayloads
from src.support.waiter import wait_until


@pytest.mark.test_script_runs
@allure.epic("LK")
@allure.feature("Script Runs")
class TestScriptRuns:

    @allure.title("Script: Company create → GET list → DELETE  (N runs)")
    @allure.description(
        "Stability scenario: POST /companies → verify appears in list → DELETE. "
        "Run with --runs=N to repeat N times in one test."
    )
    def test_company_create_get_delete_script(self, lk_api, request):
        runs = int(request.config.getoption("--runs"))
        errors: list[str] = []

        for i in range(runs):
            with allure.step(f"Run #{i + 1} of {runs}"):
                company_id = None
                try:
                    with allure.step("POST /companies — create"):
                        r = lk_api.post("/companies", json=CompanyPayloads.build_company_create_payload())
                        assert r.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
                            f"Create failed: {r.status_code} {r.text}"
                        )
                        data = r.json()
                        company_id = data.get("id") or data.get("companyID") or data.get("CompanyID")
                        assert company_id, f"No company id in response: {data}"
                        company_id = int(company_id)

                    with allure.step(f"GET /companies — verify {company_id} in list"):
                        def _in_list():
                            resp = lk_api.get("/companies")
                            if resp.status_code not in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT):
                                return None
                            items = resp.json() if resp.text else []
                            return True if any(int(c.get("id", 0)) == company_id for c in items) else None

                        found = wait_until(_in_list, timeout_s=60, step_s=3)
                        assert found is True, f"Company {company_id} not found in list within 60s"

                    with allure.step(f"DELETE /companies/{company_id}"):
                        r = lk_api.delete(f"/companies/{company_id}")
                        assert r.status_code in (
                            HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND
                        ), f"Delete failed: {r.status_code} {r.text}"

                        def _gone():
                            resp = lk_api.get("/companies")
                            if resp.status_code not in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT):
                                return None
                            items = resp.json() if resp.text else []
                            return True if not any(int(c.get("id", 0)) == company_id for c in items) else None

                        gone = wait_until(_gone, timeout_s=120, step_s=5)
                        assert gone is True, f"Company {company_id} still in list after delete"
                        company_id = None

                except Exception as exc:
                    logger.error("Run #{}: {}", i + 1, exc)
                    errors.append(f"Run #{i + 1} FAILED: {exc}")
                finally:
                    if company_id:
                        try:
                            lk_api.delete(f"/companies/{company_id}")
                        except Exception:
                            pass

        if errors:
            pytest.fail("Script run errors:\n" + "\n".join(errors), pytrace=False)
