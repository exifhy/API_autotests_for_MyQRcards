import allure
import pytest
from http import HTTPStatus

from src.constants.attributes import PHOTO_GALLERY_ATTRIBUTE_ID
from tests.e2e.employee.helpers import wait_for_photo_attr_in_0852


@allure.epic("LK")
@allure.feature("Employee")
@allure.title("Add photo gallery via CDN (>2MB) -> verify -> delete")
@pytest.mark.e2e
@pytest.mark.employee
class TestEmployeeInvitationAddPhotoCdnDeleteFlow:

    @allure.title("Employee created and 3 CDN attachments (>2MB) uploaded")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_01_employee_created(self, employee_addphoto_cdn_flow):
        assert employee_addphoto_cdn_flow["account_id"] > 0
        assert employee_addphoto_cdn_flow["invite_id"] > 0

        attachment_ids = employee_addphoto_cdn_flow["attachment_ids"]
        assert isinstance(attachment_ids, list)
        assert len(attachment_ids) == 3

        allure.attach(str(employee_addphoto_cdn_flow["invite_id"]), "invite_id", allure.attachment_type.TEXT)
        allure.attach(str(employee_addphoto_cdn_flow["account_id"]), "account_id", allure.attachment_type.TEXT)
        allure.attach("\n".join(map(str, attachment_ids)), "attachment_ids", allure.attachment_type.TEXT)

    @allure.title("PUT photo attribute (CDN attachment ids)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_02_add_photo_attributes(self, lk_api, employee_addphoto_cdn_flow):
        account_id = int(employee_addphoto_cdn_flow["account_id"])
        card_id = int(employee_addphoto_cdn_flow["card_id"])
        attachment_ids = employee_addphoto_cdn_flow["attachment_ids"]

        body = [
            {
                "AttributeID": PHOTO_GALLERY_ATTRIBUTE_ID,
                "Name": "Фото",
                "SortOrder": 1,
                "Value": [str(x) for x in attachment_ids],
                "IsEnabled": True,
                "AttributeFormID": None,
            }
        ]

        path = f"/accounts/{account_id}/cards/{card_id}/attributes"
        with allure.step(f"PUT {path}"):
            response = lk_api.session.put(lk_api.base_url + path, json=body)
            allure.attach(str(response.status_code), "put_status", allure.attachment_type.TEXT)
            if response.text:
                allure.attach(response.text, "put_response_text", allure.attachment_type.TEXT)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"PUT attributes failed: {response.status_code} {response.text}"
        )

    @allure.title("Photo visible via 085.2 (CDN)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_03_photo_visible_in_0852(self, lk_api, employee_addphoto_cdn_flow):
        account_id = int(employee_addphoto_cdn_flow["account_id"])
        card_id = int(employee_addphoto_cdn_flow["card_id"])
        attachment_ids = employee_addphoto_cdn_flow["attachment_ids"]

        with allure.step("Wait until photo attribute appears in 085.2"):
            ok = wait_for_photo_attr_in_0852(
                lk_api,
                account_id=account_id,
                card_id=card_id,
                attachment_ids=attachment_ids,
                timeout_s=120,
                step_s=5,
            )

        assert ok, (
            f"Photo attribute id={PHOTO_GALLERY_ATTRIBUTE_ID} "
            "with CDN-uploaded values not visible in 085.2"
        )

    @allure.title("Delete invitation (CDN photo flow)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_04_delete_employee(self, lk_api, employee_addphoto_cdn_flow):
        sub_id = int(employee_addphoto_cdn_flow["subscription_id"])
        invite_id = int(employee_addphoto_cdn_flow["invite_id"])

        path = f"/Subscriptions/{sub_id}/invitation/{invite_id}"
        with allure.step(f"DELETE {path}"):
            response = lk_api.delete(path)
            allure.attach(str(response.status_code), "delete_status", allure.attachment_type.TEXT)
            if response.text:
                allure.attach(response.text, "delete_response_text", allure.attachment_type.TEXT)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Delete failed: {response.status_code} {response.text}"
        )
        employee_addphoto_cdn_flow["deleted"] = True
