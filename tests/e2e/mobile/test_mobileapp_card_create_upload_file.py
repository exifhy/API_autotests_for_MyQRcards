import allure
import pytest
from http import HTTPStatus

from src.constants.attributes import EMAIL_ATTRIBUTE_ID, FILE_ATTRIBUTE_ID, PHONE_ATTRIBUTE_ID
from src.resources.mobile_api import (
    create_mobile_card,
    delete_mobile_card,
    list_mobile_card_attributes,
    merge_mobile_card_attributes,
    upload_mobile_attachment,
    upload_mobile_attachment_v2,
)
from tests.e2e.mobile.helpers import (
    extract_mobile_attachment_id,
    wait_mobile_attr_values,
    wait_mobile_card_ready,
)


@allure.epic("Mobile APP")
@allure.feature("Cards")
@allure.title("Create card -> Upload file attribute -> Delete")
@pytest.mark.mobile
@pytest.mark.e2e
class TestMobileAppCardCreateUploadFile:
    @allure.title("Upload card photo")
    def test_01_upload_photo(self, mobile_api, mobile_file_flow):
        response = upload_mobile_attachment(
            mobile_api,
            file_path=mobile_file_flow["media"]["photo_path"],
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED), (
            f"Photo upload failed: {response.status_code}, body={response.text}"
        )
        mobile_file_flow["attachment_id"] = extract_mobile_attachment_id(response)

    @allure.title("Create mobile card")
    def test_02_create_card(self, mobile_api, mobile_file_flow):
        attachment_id = mobile_file_flow["attachment_id"]
        assert attachment_id, "attachment_id empty (test_01 failed?)"

        response = create_mobile_card(
            mobile_api,
            mobile_file_flow["payload"],
            attachment_id,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
            f"Create card failed: {response.status_code}, body={response.text}"
        )

        card_id = response.json().get("id")
        assert card_id, f"No card id in response: {response.text}"
        mobile_file_flow["card_id"] = int(card_id)

    @allure.title("Get card after create")
    def test_03_get_card_after_create(self, mobile_api, mobile_file_flow):
        card_id = mobile_file_flow["card_id"]
        assert card_id, "card_id empty (test_02 failed?)"
        response = wait_mobile_card_ready(mobile_api, card_id)
        assert response.status_code == HTTPStatus.OK, (
            f"GET card failed: {response.status_code}, body={response.text}"
        )

    @allure.title("Merge phone and email")
    def test_04_merge_phone_email(self, mobile_api, mobile_file_flow):
        card_id = mobile_file_flow["card_id"]
        assert card_id, "card_id empty (test_02 failed?)"

        body = [
            {
                "AttributeID": PHONE_ATTRIBUTE_ID,
                "Name": "Мобильный телефон",
                "SortOrder": 1,
                "IsEnabled": True,
                "Value": [mobile_file_flow["expected"]["phone"]],
            },
            {
                "AttributeID": EMAIL_ATTRIBUTE_ID,
                "Name": "Электронная почта",
                "SortOrder": 2,
                "IsEnabled": True,
                "Value": [mobile_file_flow["expected"]["email"]],
            },
        ]
        response = merge_mobile_card_attributes(mobile_api, card_id, body)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Merge phone/email failed: {response.status_code}, body={response.text}"
        )

    @allure.title("Attributes list has phone and email")
    def test_05_attrs_have_phone_email(self, mobile_api, mobile_file_flow):
        card_id = mobile_file_flow["card_id"]
        assert card_id, "card_id empty (test_02 failed?)"

        items = wait_mobile_attr_values(
            mobile_api,
            card_id,
            expected_values=[
                mobile_file_flow["expected"]["phone"],
                mobile_file_flow["expected"]["email"],
            ],
            timeout_s=60,
            step_s=3,
        )
        assert items is not None, "Phone/email values not found in attributes list"

    @allure.title("Upload document and merge file attribute")
    def test_06_upload_doc_and_merge_file(self, mobile_api, mobile_file_flow):
        card_id = mobile_file_flow["card_id"]
        assert card_id, "card_id empty (test_02 failed?)"

        response = upload_mobile_attachment_v2(
            mobile_api,
            file_path=mobile_file_flow["media"]["doc_path"],
            attribute_id=FILE_ATTRIBUTE_ID,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED), (
            f"Document upload failed: {response.status_code}, body={response.text}"
        )
        mobile_file_flow["doc_attachment_id"] = extract_mobile_attachment_id(response)

        body = [
            {
                "AttributeID": FILE_ATTRIBUTE_ID,
                "Name": "Файл",
                "SortOrder": 3,
                "IsEnabled": True,
                "Value": [str(mobile_file_flow["doc_attachment_id"])],
            }
        ]
        merge_response = merge_mobile_card_attributes(mobile_api, card_id, body)
        assert merge_response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Merge file attribute failed: {merge_response.status_code}, body={merge_response.text}"
        )

    @allure.title("Attributes list has file attribute")
    def test_07_attrs_have_file(self, mobile_api, mobile_file_flow):
        card_id = mobile_file_flow["card_id"]
        doc_attachment_id = mobile_file_flow["doc_attachment_id"]
        assert card_id, "card_id empty (test_02 failed?)"
        assert doc_attachment_id, "doc_attachment_id empty (test_06 failed?)"

        items = wait_mobile_attr_values(
            mobile_api,
            card_id,
            expected_values=[str(doc_attachment_id)],
            expected_name="Файл",
            timeout_s=60,
            step_s=3,
        )
        assert items is not None, "File attribute not found by name and value"

    @allure.title("Delete mobile card")
    def test_08_delete_card(self, mobile_api, mobile_file_flow):
        card_id = mobile_file_flow["card_id"]
        assert card_id, "card_id empty (test_02 failed?)"
        response = delete_mobile_card(mobile_api, card_id)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Delete card failed: {response.status_code}, body={response.text}"
        )
        mobile_file_flow["deleted"] = True
