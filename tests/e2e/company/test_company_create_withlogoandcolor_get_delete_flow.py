import allure
import pytest
from http import HTTPStatus

from services.companies.company_create.payloads import Payloads as CreatePayloads
from services.companies.company_update.payloads import Payloads as UpdatePayloads
from src.resources.uploads import upload_generated_image
from src.support.waiter import wait_until
from src.utils.randoms import rand_hex_color


@allure.epic("LK")
@allure.feature("Company")
@pytest.mark.company
@pytest.mark.e2e
@allure.description("/Companies — create, upload logo + background, set design, delete flow")
class TestCompanyCreateWithLogoAndColorFlow:

    @allure.title("POST /Companies → list → upload logo → update → GET → upload bg → designsettings → GET → DELETE")
    @pytest.mark.smoke
    def test_company_create_withlogoandcolor_get_delete_flow(self, lk_api, cfg):
        company_id = None
        try:
            with allure.step("01. POST /companies — create company"):
                create_payload = CreatePayloads.build_company_create_payload()
                r = lk_api.post("/companies", json=create_payload)
                assert r.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
                    f"Create failed: {r.status_code} {r.text}"
                )
                data = r.json()
                company_id = data.get("id") or data.get("companyID") or data.get("CompanyID")
                assert company_id, f"No company id in response: {data}"
                company_id = int(company_id)

            with allure.step(f"02. GET /companies — company {company_id} appears in list"):
                def _in_list():
                    resp = lk_api.get("/companies")
                    if resp.status_code not in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT):
                        return None
                    items = resp.json() if resp.text else []
                    return True if any(int(c.get("id", 0)) == company_id for c in items) else None

                found = wait_until(_in_list, timeout_s=60, step_s=3)
                assert found is True, f"Company {company_id} not found in GET /companies within 60s"

            with allure.step("03. POST /attachments — upload logo (PNG)"):
                logo_id = upload_generated_image(lk_api, cfg, fmt="png", label="company logo")
                assert logo_id > 0, f"Logo attachment id is invalid: {logo_id}"

            with allure.step(f"04. PUT /companies/{company_id} — attach logo"):
                update_payload = UpdatePayloads.build_company_update_payload()
                update_payload["LogoAttachmentID"] = logo_id
                r = lk_api.put(f"/companies/{company_id}", json=update_payload)
                assert r.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
                    f"Update with logo failed: {r.status_code} {r.text}"
                )

            with allure.step(f"05. GET /companies/{company_id} — verify logo applied"):
                def _logo_applied():
                    resp = lk_api.get(f"/companies/{company_id}")
                    if resp.status_code != HTTPStatus.OK:
                        return None
                    body = resp.json()
                    logo = body.get("logo") or {}
                    return body if logo.get("id") == logo_id else None

                verified = wait_until(_logo_applied, timeout_s=60, step_s=3)
                assert verified is not None, (
                    f"Logo id={logo_id} not reflected in GET /companies/{company_id} within 60s"
                )

            with allure.step("06. POST /attachments — upload background (JPEG)"):
                bg_id = upload_generated_image(lk_api, cfg, fmt="jpeg", label="company background")
                assert bg_id > 0, f"Background attachment id is invalid: {bg_id}"

            with allure.step(f"07. PUT /companies/{company_id}/designsettings — set color and background"):
                color = rand_hex_color()
                qr_color = rand_hex_color()
                design_payload = {
                    "Color": color,
                    "QRColor": qr_color,
                    "BackgroundAttachmentID": bg_id,
                }
                r = lk_api.put(f"/companies/{company_id}/designsettings", json=design_payload)
                assert r.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
                    f"Designsettings update failed: {r.status_code} {r.text}"
                )

            with allure.step(f"08. GET /companies/{company_id}/designsettings — verify color and background"):
                def _design_applied():
                    resp = lk_api.get(f"/companies/{company_id}/designsettings")
                    if resp.status_code != HTTPStatus.OK:
                        return None
                    body = resp.json()
                    color_ok = body.get("color") == color
                    qr_ok = body.get("qrColor") == qr_color
                    bg_ok = body.get("backgroundAttachmentID") == bg_id
                    return body if (color_ok and qr_ok and bg_ok) else None

                verified = wait_until(_design_applied, timeout_s=60, step_s=3)
                assert verified is not None, (
                    f"Designsettings not applied for company {company_id} within 60s. "
                    f"Expected color={color}, qrColor={qr_color}, backgroundAttachmentID={bg_id}"
                )

            with allure.step(f"09. DELETE /companies/{company_id} — delete company"):
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
