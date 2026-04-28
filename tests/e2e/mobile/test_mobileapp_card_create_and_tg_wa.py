import allure
import pytest
from http import HTTPStatus

from src.constants.attributes import TELEGRAM_ATTRIBUTE_ID, WHATSAPP_ATTRIBUTE_ID
from src.resources.mobile_api import (
    create_mobile_card,
    delete_mobile_card_with_retry,
    merge_mobile_card_attributes,
)
from tests.e2e.mobile.helpers import wait_mobile_attr_values, wait_mobile_card_ready


@allure.epic("Mobile APP")
@allure.feature("Cards")
@allure.title("Create card -> Add tg/wa -> Delete")
@pytest.mark.mobile
@pytest.mark.e2e
class TestMobileAppCardCreateAndTgWa:
    @allure.title("Create mobile card returns id")
    def test_01_create_card(self, mobile_api, mobile_tg_wa_flow):
        response = mobile_api.post("/cards/V2.0", json=mobile_tg_wa_flow["payload"])
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
            f"Create card failed: {response.status_code}, body={response.text}"
        )

        card_id = response.json().get("id")
        assert card_id, f"No card id in response: {response.text}"
        mobile_tg_wa_flow["card_id"] = int(card_id)

    @allure.title("Mobile card GET returns 200")
    def test_02_get_card_after_create(self, mobile_api, mobile_tg_wa_flow):
        card_id = mobile_tg_wa_flow["card_id"]
        assert card_id, "card_id empty (test_01 failed?)"
        response = wait_mobile_card_ready(mobile_api, card_id)
        assert response is not None, f"GET card failed or not ready: card_id={card_id}"

    @allure.title("Merge tg and wa attributes")
    def test_03_merge_tg_wa(self, mobile_api, mobile_tg_wa_flow):
        card_id = mobile_tg_wa_flow["card_id"]
        assert card_id, "card_id empty (test_01 failed?)"

        body = [
            {
                "AttributeID": TELEGRAM_ATTRIBUTE_ID,
                "Name": "Telegram",
                "SortOrder": 3,
                "IsEnabled": True,
                "Value": [mobile_tg_wa_flow["expected"]["tg"]],
            },
            {
                "AttributeID": WHATSAPP_ATTRIBUTE_ID,
                "Name": "WhatsApp",
                "SortOrder": 4,
                "IsEnabled": True,
                "Value": [mobile_tg_wa_flow["expected"]["wa"]],
            },
        ]

        response = merge_mobile_card_attributes(mobile_api, card_id, body)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Merge tg/wa failed: {response.status_code}, body={response.text}"
        )

    @allure.title("Attributes list contains tg and wa")
    def test_04_attributes_list_contains_tg_wa(self, mobile_api, mobile_tg_wa_flow):
        card_id = mobile_tg_wa_flow["card_id"]
        assert card_id, "card_id empty (test_01 failed?)"
        found = wait_mobile_attr_values(
            mobile_api,
            card_id,
            expected_values=[
                mobile_tg_wa_flow["expected"]["tg"],
                mobile_tg_wa_flow["expected"]["wa"],
            ],
            enabled_only=True,
            timeout_s=60,
            step_s=3,
        )
        assert found is not None, "Telegram/WhatsApp values not found in attributes list"

    @allure.title("Delete mobile card")
    def test_05_delete_card(self, mobile_api, mobile_tg_wa_flow):
        card_id = mobile_tg_wa_flow["card_id"]
        assert card_id, "card_id empty (test_01 failed?)"

        response = delete_mobile_card_with_retry(
            mobile_api,
            card_id,
            attempts=5,
            step_s=2.0,
        )
        assert response is not None, "No response from delete"
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND, HTTPStatus.GONE), (
            f"Delete card failed: {response.status_code}, body={getattr(response, 'text', '')}"
        )
        mobile_tg_wa_flow["deleted"] = True
