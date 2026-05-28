import allure
import pytest
from http import HTTPStatus

from services.companies.company_create.payloads import Payloads as CreatePayloads
from services.companies.company_update.payloads import Payloads as UpdatePayloads
from src.support.waiter import wait_until


@allure.epic("LK")
@allure.feature("Company")
@pytest.mark.company
@pytest.mark.e2e
@allure.description("/Companies — create, edit, get, delete flow")
class TestCompanyCreateEditDeleteFlow:

    @allure.title("POST /Companies → GET → PUT → GET → DELETE")
    @pytest.mark.smoke
    def test_company_create_edit_delete_flow(self, lk_api):
        company_id = None
        try:
            with allure.step("01. POST /Companies — create company"):
                create_payload = CreatePayloads.build_company_create_payload()
                r = lk_api.post("/companies", json=create_payload)
                assert r.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
                    f"Create failed: {r.status_code} {r.text}"
                )
                data = r.json()
                company_id = data.get("id") or data.get("companyID") or data.get("CompanyID")
                assert company_id, f"No company id in response: {data}"
                company_id = int(company_id)

            with allure.step(f"02. GET /companies/{company_id} — verify company exists"):
                def _created():
                    resp = lk_api.get(f"/companies/{company_id}")
                    if resp.status_code != HTTPStatus.OK:
                        return None
                    body = resp.json()
                    return body if body.get("name") == create_payload["Name"] else None

                found = wait_until(_created, timeout_s=60, step_s=3)
                assert found is not None, (
                    f"Company '{create_payload['Name']}' not found at GET /companies/{company_id} within 60s"
                )

            with allure.step(f"03. PUT /companies/{company_id} — update company name"):
                update_payload = UpdatePayloads.build_company_update_payload()
                r = lk_api.put(f"/companies/{company_id}", json=update_payload)
                assert r.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
                    f"Update failed: {r.status_code} {r.text}"
                )

            with allure.step(f"04. GET /companies/{company_id} — verify name updated"):
                def _updated():
                    resp = lk_api.get(f"/companies/{company_id}")
                    if resp.status_code != HTTPStatus.OK:
                        return None
                    body = resp.json()
                    return body if body.get("name") == update_payload["Name"] else None

                updated = wait_until(_updated, timeout_s=60, step_s=3)
                assert updated is not None, (
                    f"Company name not updated to '{update_payload['Name']}' within 60s"
                )

            with allure.step(f"05. DELETE /companies/{company_id} — delete company"):
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
                assert gone is True, f"Company {company_id} still appears in GET /companies after delete"
                company_id = None

        finally:
            if company_id:
                try:
                    lk_api.delete(f"/companies/{company_id}")
                except Exception:
                    pass
