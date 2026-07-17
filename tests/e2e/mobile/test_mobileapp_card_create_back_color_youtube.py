import allure
import pytest
from http import HTTPStatus

from src.constants.attributes import YOUTUBE_ATTRIBUTE_ID
from src.resources.mobile_api import (
    delete_mobile_card,
    list_mobile_cards_v2,
    merge_mobile_card_attributes,
    merge_mobile_designsettings,
    upload_mobile_attachment_v2,
)
from tests.e2e.mobile.builders import (
    build_mobile_attribute_body,
    build_mobile_designsettings_body,
    rand_hex_color,
    rand_youtube_url,
)
from tests.e2e.mobile.helpers import (
    extract_mobile_attachment_id,
    wait_mobile_attr_values,
    wait_mobile_card_ready,
    wait_mobile_designsettings_contains,
)


@allure.epic("Mobile APP")
@allure.feature("Cards")
@allure.title("Create card -> Background/color -> YouTube -> Delete")
@pytest.mark.mobile
@pytest.mark.e2e
class TestMobileAppCardCreateBackColorYoutube:
    @allure.title("Create mobile card")
    def test_01_create_card(self, mobile_api, mobile_back_color_youtube_flow):
        response = mobile_api.post("/cards/V2.0", json=mobile_back_color_youtube_flow["payload"])
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
            f"Create card failed: {response.status_code}, body={response.text}"
        )
        card_id = response.json().get("id")
        assert card_id, f"No card id in response: {response.text}"
        mobile_back_color_youtube_flow["card_id"] = int(card_id)

    @allure.title("Get card after create")
    def test_02_get_card_after_create(self, mobile_api, mobile_back_color_youtube_flow):
        card_id = mobile_back_color_youtube_flow["card_id"]
        assert card_id, "card_id empty (test_01 failed?)"
        response = wait_mobile_card_ready(mobile_api, card_id)
        assert response is not None, f"GET card failed or not ready (card_id={card_id})"

    @allure.title("Upload back photo")
    def test_03_upload_back_photo(self, mobile_api, mobile_back_color_youtube_flow):
        response = upload_mobile_attachment_v2(
            mobile_api,
            file_path=mobile_back_color_youtube_flow["media"]["back_path"],
            attribute_id=YOUTUBE_ATTRIBUTE_ID,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED), (
            f"Back image upload failed: {response.status_code}, body={response.text}"
        )
        mobile_back_color_youtube_flow["background_attachment_id"] = extract_mobile_attachment_id(response)

    @allure.title("Set designsettings background")
    def test_04_merge_designsettings_background(self, mobile_api, mobile_back_color_youtube_flow):
        card_id = mobile_back_color_youtube_flow["card_id"]
        attachment_id = mobile_back_color_youtube_flow["background_attachment_id"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert attachment_id, "background_attachment_id empty (test_03 failed?)"

        body = build_mobile_designsettings_body(
            color=mobile_back_color_youtube_flow["expected"]["base_color"],
            background_attachment_id=attachment_id,
        )
        response = merge_mobile_designsettings(mobile_api, card_id, body)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Designsettings merge failed: {response.status_code}, body={response.text}"
        )

    @allure.title("Designsettings has background")
    def test_05_get_designsettings_has_background(self, mobile_api, mobile_back_color_youtube_flow):
        card_id = mobile_back_color_youtube_flow["card_id"]
        expected_att = str(mobile_back_color_youtube_flow["background_attachment_id"])
        assert card_id, "card_id empty (test_01 failed?)"

        data = wait_mobile_designsettings_contains(
            mobile_api,
            card_id,
            expected_att,
            timeout_s=60,
            step_s=3,
        )
        assert data is not None, f"BackgroundAttachmentID not found: {expected_att}"

    @allure.title("057 Cards/ListV2 has background fields (REQUIREMENT 31890)")
    def test_05a_cards_listv2_has_background(self, mobile_api, mobile_back_color_youtube_flow):
        card_id = mobile_back_color_youtube_flow["card_id"]
        attachment_id = mobile_back_color_youtube_flow["background_attachment_id"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert attachment_id, "background_attachment_id empty (test_03 failed?)"

        response = list_mobile_cards_v2(mobile_api)
        assert response.status_code == HTTPStatus.OK, (
            f"Cards/ListV2 failed: {response.status_code}, body={response.text}"
        )
        cards = response.json()
        card = next((c for c in cards if c.get("id") == card_id), None)
        assert card is not None, f"Card {card_id} not found in Cards/ListV2 response"

        background_attachment = card.get("backgroundAttachment") or {}
        assert background_attachment.get("id") == attachment_id, (
            f"Expected backgroundAttachment.id={attachment_id}, got {background_attachment.get('id')}"
        )
        assert background_attachment.get("url"), (
            f"backgroundAttachment.url missing/empty for card {card_id}: {card}"
        )

    @allure.title("Change designsettings color")
    def test_06_merge_designsettings_change_color(self, mobile_api, mobile_back_color_youtube_flow):
        card_id = mobile_back_color_youtube_flow["card_id"]
        attachment_id = mobile_back_color_youtube_flow["background_attachment_id"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert attachment_id, "background_attachment_id empty (test_03 failed?)"

        new_color = rand_hex_color()
        mobile_back_color_youtube_flow["color_2"] = new_color
        body = build_mobile_designsettings_body(
            color=new_color,
            background_attachment_id=attachment_id,
        )
        response = merge_mobile_designsettings(mobile_api, card_id, body)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Designsettings color merge failed: {response.status_code}, body={response.text}"
        )

    @allure.title("Designsettings has new color")
    def test_07_get_designsettings_has_new_color(self, mobile_api, mobile_back_color_youtube_flow):
        card_id = mobile_back_color_youtube_flow["card_id"]
        expected_color = mobile_back_color_youtube_flow["color_2"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert expected_color, "color_2 empty (test_06 failed?)"

        data = wait_mobile_designsettings_contains(
            mobile_api,
            card_id,
            expected_color,
            timeout_s=60,
            step_s=3,
        )
        assert data is not None, f"Color not changed to {expected_color}"

    @allure.title("Merge YouTube attribute")
    def test_08_merge_youtube_attr(self, mobile_api, mobile_back_color_youtube_flow):
        card_id = mobile_back_color_youtube_flow["card_id"]
        assert card_id, "card_id empty (test_01 failed?)"

        youtube_url = rand_youtube_url()
        mobile_back_color_youtube_flow["youtube_url"] = youtube_url
        body = build_mobile_attribute_body(
            attribute_id=YOUTUBE_ATTRIBUTE_ID,
            name="YouTube",
            sort_order=1,
            value=[youtube_url],
            attribute_form_id=None,
        )
        response = merge_mobile_card_attributes(mobile_api, card_id, body)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Merge YouTube failed: {response.status_code}, body={response.text}"
        )

    @allure.title("085 has YouTube attribute")
    def test_09_attrs_have_youtube(self, mobile_api, mobile_back_color_youtube_flow):
        card_id = mobile_back_color_youtube_flow["card_id"]
        expected_url = mobile_back_color_youtube_flow["youtube_url"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert expected_url, "youtube_url empty (test_08 failed?)"

        items = wait_mobile_attr_values(
            mobile_api,
            card_id,
            expected_values=[expected_url],
            expected_name="YouTube",
            timeout_s=120,
            step_s=3,
        )
        assert items is not None, f"YouTube attribute not found by name+url ({expected_url})"

    @allure.title("Delete mobile card")
    def test_10_delete_card(self, mobile_api, mobile_back_color_youtube_flow):
        card_id = mobile_back_color_youtube_flow["card_id"]
        assert card_id, "card_id empty (test_01 failed?)"
        response = delete_mobile_card(mobile_api, card_id)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Delete card failed: {response.status_code}, body={response.text}"
        )
        mobile_back_color_youtube_flow["deleted"] = True
