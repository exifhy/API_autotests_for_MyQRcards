import allure
import pytest
from http import HTTPStatus

from src.constants.attributes import EMAIL_ATTRIBUTE_ID, PHONE_ATTRIBUTE_ID
from src.resources.mobile_api import (
    create_mobile_card,
    delete_mobile_card,
    list_mobile_card_attributes,
    merge_mobile_card_attributes,
    upload_mobile_attachment,
)
from tests.e2e.mobile.helpers import (
    extract_mobile_attachment_id,
    wait_mobile_attr_values,
    wait_mobile_card_ready,
)


@allure.epic("Mobile APP")
@allure.feature("Cards")
@allure.title("Create card -> Add attributes -> Delete")
@pytest.mark.mobile
@pytest.mark.e2e
class TestMobileAppCardCreate:
    @allure.title("Upload mobile photo")
    def test_01_upload_mobile_photo(self, mobile_api, mobile_card_create_flow):
        response = upload_mobile_attachment(
            mobile_api,
            file_path=mobile_card_create_flow["media"]["photo_path"],
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED), (
            f"Upload failed: {response.status_code}, body={response.text}"
        )
        mobile_card_create_flow["attachment_id"] = extract_mobile_attachment_id(response)

    @allure.title("Create mobile card returns id")
    def test_02_create_card_returns_id(self, mobile_api, mobile_card_create_flow):
        attachment_id = mobile_card_create_flow["attachment_id"]
        assert attachment_id, "attachment_id empty (test_01 failed?)"

        response = create_mobile_card(
            mobile_api,
            mobile_card_create_flow["payload"],
            attachment_id,
        )
        assert response is not None, "Create card returned no response"
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
            f"Create card failed: {response.status_code}, body={response.text}"
        )

        card_id = response.json().get("id")
        assert card_id, f"No card id in response: {response.text}"
        mobile_card_create_flow["card_id"] = int(card_id)

    @allure.title("Mobile card GET returns 200")
    def test_03_get_card_returns_200(self, mobile_api, mobile_card_create_flow):
        card_id = mobile_card_create_flow["card_id"]
        assert card_id, "card_id empty (test_02 failed?)"
        response = wait_mobile_card_ready(mobile_api, card_id)
        assert response is not None, f"GET card failed or not ready (card_id={card_id})"

    @allure.title("Merge phone and email attributes")
    def test_04_merge_attributes(self, mobile_api, mobile_card_create_flow):
        card_id = mobile_card_create_flow["card_id"]
        assert card_id, "card_id empty (test_02 failed?)"

        body = [
            {
                "AttributeID": PHONE_ATTRIBUTE_ID,
                "Name": "Мобильный телефон",
                "SortOrder": 1,
                "IsEnabled": True,
                "Value": [mobile_card_create_flow["expected"]["phone"]],
            },
            {
                "AttributeID": EMAIL_ATTRIBUTE_ID,
                "Name": "Электронная почта",
                "SortOrder": 2,
                "IsEnabled": True,
                "Value": [mobile_card_create_flow["expected"]["email"]],
            },
        ]

        response = merge_mobile_card_attributes(mobile_api, card_id, body)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Merge attributes failed: {response.status_code}, body={response.text}"
        )

    @allure.title("Attributes list contains phone and email")
    def test_05_attributes_list_contains_values(self, mobile_api, mobile_card_create_flow):
        card_id = mobile_card_create_flow["card_id"]
        assert card_id, "card_id empty (test_02 failed?)"
        found = wait_mobile_attr_values(
            mobile_api,
            card_id,
            expected_values=[
                mobile_card_create_flow["expected"]["phone"],
                mobile_card_create_flow["expected"]["email"],
            ],
            enabled_only=True,
            timeout_s=60,
            step_s=3,
        )
        assert found is not None, "Phone/email attributes not found in card attributes list"

    @allure.title("Delete mobile card")
    def test_06_delete_card(self, mobile_api, mobile_card_create_flow):
        card_id = mobile_card_create_flow["card_id"]
        assert card_id, "card_id empty (test_02 failed?)"

        response = delete_mobile_card(mobile_api, card_id)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Delete card failed: {response.status_code}, body={response.text}"
        )
        mobile_card_create_flow["deleted"] = True
