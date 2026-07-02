import allure
import pytest
from http import HTTPStatus

from services.companies.company_create.payloads import Payloads as CreatePayloads
from services.companies.company_update.payloads import Payloads as UpdatePayloads
from src.resources.uploads import upload_large_image_cdn
from src.support.waiter import wait_until
from src.utils.randoms import rand_hex_color


@allure.epic("LK")
@allure.feature("Company")
@pytest.mark.company
@pytest.mark.e2e
@allure.description(
    "Создание компании с логотипом и фоном >2МБ через CDN endpoint (POST /attachments/v2/)"
)
class TestCompanyCreateWithLargeCdnImagesFlow:

    @allure.title("POST /Companies → CDN upload logo (>2МБ) → CDN upload bg (>2МБ) → designsettings → DELETE")
    def test_company_create_with_large_cdn_images_flow(self, lk_api, cfg):
        company_id = None
        try:
            with allure.step("01. POST /companies — создать компанию"):
                create_payload = CreatePayloads.build_company_create_payload()
                r = lk_api.post("/companies", json=create_payload)
                assert r.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
                    f"Create failed: {r.status_code} {r.text}"
                )
                data = r.json()
                company_id = data.get("id") or data.get("companyID") or data.get("CompanyID")
                assert company_id, f"No company id in response: {data}"
                company_id = int(company_id)

            with allure.step(f"02. GET /companies — company {company_id} в списке"):
                def _in_list():
                    resp = lk_api.get("/companies")
                    if resp.status_code not in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT):
                        return None
                    items = resp.json() if resp.text else []
                    return True if any(int(c.get("id", 0)) == company_id for c in items) else None

                assert wait_until(_in_list, timeout_s=60, step_s=3) is True, (
                    f"Company {company_id} not found in GET /companies within 60s"
                )

            with allure.step("03. CDN upload logo PNG >2МБ"):
                logo_id = upload_large_image_cdn(label="company logo large", target_size_mb=2.0)
                assert logo_id > 0, f"Logo CDN attachment id invalid: {logo_id}"

            with allure.step(f"04. PUT /companies/{company_id} — установить логотип"):
                update_payload = UpdatePayloads.build_company_update_payload()
                update_payload["LogoAttachmentID"] = logo_id
                r = lk_api.put(f"/companies/{company_id}", json=update_payload)
                assert r.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
                    f"Update with logo failed: {r.status_code} {r.text}"
                )

            with allure.step(f"05. GET /companies/{company_id} — логотип применён"):
                def _logo_applied():
                    resp = lk_api.get(f"/companies/{company_id}")
                    if resp.status_code != HTTPStatus.OK:
                        return None
                    logo = resp.json().get("logo") or {}
                    return resp.json() if logo.get("id") == logo_id else None

                assert wait_until(_logo_applied, timeout_s=60, step_s=3) is not None, (
                    f"Logo id={logo_id} not reflected in GET /companies/{company_id} within 60s"
                )

            with allure.step("06. CDN upload background JPEG >2МБ"):
                bg_id = upload_large_image_cdn(label="company bg large", target_size_mb=2.0)
                assert bg_id > 0, f"Background CDN attachment id invalid: {bg_id}"

            with allure.step(f"07. PUT /companies/{company_id}/designsettings — цвет и фон"):
                color = rand_hex_color()
                qr_color = rand_hex_color()
                r = lk_api.put(f"/companies/{company_id}/designsettings", json={
                    "Color": color,
                    "QRColor": qr_color,
                    "BackgroundAttachmentID": bg_id,
                })
                assert r.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
                    f"Designsettings update failed: {r.status_code} {r.text}"
                )

            with allure.step(f"08. GET /companies/{company_id}/designsettings — фон применён"):
                def _design_applied():
                    resp = lk_api.get(f"/companies/{company_id}/designsettings")
                    if resp.status_code != HTTPStatus.OK:
                        return None
                    body = resp.json()
                    return body if (
                        body.get("color") == color
                        and body.get("qrColor") == qr_color
                        and body.get("backgroundAttachmentID") == bg_id
                    ) else None

                assert wait_until(_design_applied, timeout_s=60, step_s=3) is not None, (
                    f"Designsettings not applied for company {company_id} within 60s"
                )

            with allure.step(f"09. DELETE /companies/{company_id}"):
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

                assert wait_until(_gone, timeout_s=120, step_s=5) is True, (
                    f"Company {company_id} still in list after delete"
                )
                company_id = None

        finally:
            if company_id:
                try:
                    lk_api.delete(f"/companies/{company_id}")
                except Exception:
                    pass
