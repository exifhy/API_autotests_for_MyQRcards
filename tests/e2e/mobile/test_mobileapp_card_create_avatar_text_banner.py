import allure
import pytest
from http import HTTPStatus

from src.constants.attributes import AVATAR_ATTRIBUTE_ID_V2, BANNER_ATTRIBUTE_ID, TEXT_ATTRIBUTE_ID
from src.resources.mobile_api import (
    delete_mobile_card,
    merge_mobile_card_attributes,
    update_mobile_card_v2,
    upload_mobile_attachment_v2,
)
from tests.e2e.mobile.builders import (
    build_mobile_attribute_body,
    build_mobile_avatar_update_payload,
    rand_space_text,
    rand_word,
)
from tests.e2e.mobile.helpers import (
    extract_mobile_attachment_id,
    wait_mobile_attr_values,
    wait_mobile_card_ready,
    wait_mobile_gallery_has_attachment,
)


@allure.epic("Mobile APP")
@allure.feature("Cards")
@allure.title("Create card -> Avatar -> Text -> Banner -> Delete")
@pytest.mark.mobile
@pytest.mark.e2e
class TestMobileAppCardCreateAvatarTextBanner:
    @allure.title("Create mobile card")
    def test_01_create_card(self, mobile_api, mobile_avatar_text_banner_flow):
        response = mobile_api.post("/cards/V2.0", json=mobile_avatar_text_banner_flow["payload"])
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
            f"Create card failed: {response.status_code}, body={response.text}"
        )
        card_id = response.json().get("id")
        assert card_id, f"No card id in response: {response.text}"
        mobile_avatar_text_banner_flow["card_id"] = int(card_id)

    @allure.title("Get card after create")
    def test_02_get_card_after_create(self, mobile_api, mobile_avatar_text_banner_flow):
        card_id = mobile_avatar_text_banner_flow["card_id"]
        assert card_id, "card_id empty (test_01 failed?)"
        response = wait_mobile_card_ready(mobile_api, card_id)
        assert response is not None, f"GET card failed after create (card_id={card_id})"

    @allure.title("Upload avatar photo")
    def test_03_upload_avatar_photo(self, mobile_api, mobile_avatar_text_banner_flow):
        response = upload_mobile_attachment_v2(
            mobile_api,
            file_path=mobile_avatar_text_banner_flow["media"]["photo_path"],
            attribute_id=AVATAR_ATTRIBUTE_ID_V2,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED), (
            f"Avatar upload failed: {response.status_code}, body={response.text}"
        )
        mobile_avatar_text_banner_flow["avatar_attachment_id"] = extract_mobile_attachment_id(response)

    @allure.title("Set avatar via card update")
    def test_04_set_avatar_via_update(self, mobile_api, mobile_avatar_text_banner_flow):
        card_id = mobile_avatar_text_banner_flow["card_id"]
        attachment_id = mobile_avatar_text_banner_flow["avatar_attachment_id"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert attachment_id, "avatar_attachment_id empty (test_03 failed?)"

        payload = build_mobile_avatar_update_payload(attachment_id=attachment_id)
        response = update_mobile_card_v2(mobile_api, card_id, payload)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Update avatar failed: {response.status_code}, body={response.text}"
        )

    @allure.title("Get card gallery has avatar")
    def test_05_get_card_gallery_has_avatar(self, mobile_api, mobile_avatar_text_banner_flow):
        card_id = mobile_avatar_text_banner_flow["card_id"]
        attachment_id = mobile_avatar_text_banner_flow["avatar_attachment_id"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert attachment_id, "avatar_attachment_id empty (test_03 failed?)"

        card_json = wait_mobile_gallery_has_attachment(
            mobile_api,
            card_id,
            attachment_id,
            timeout_s=90,
            step_s=3,
        )
        assert card_json is not None, (
            f"Card gallery does not contain avatar attachment id={attachment_id}"
        )

    @allure.title("Merge text attribute")
    def test_06_merge_text(self, mobile_api, mobile_avatar_text_banner_flow):
        card_id = mobile_avatar_text_banner_flow["card_id"]
        assert card_id, "card_id empty (test_01 failed?)"

        text_value = rand_space_text(30)
        mobile_avatar_text_banner_flow["text_value"] = text_value

        body = build_mobile_attribute_body(
            attribute_id=TEXT_ATTRIBUTE_ID,
            name="РњРёРЅРё СЂР°СЃСЃРєР°Р·",
            sort_order=1,
            value=[text_value],
        )
        response = merge_mobile_card_attributes(mobile_api, card_id, body)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Merge text failed: {response.status_code}, body={response.text}"
        )

    @allure.title("085 has text attribute")
    def test_07_attrs_have_text(self, mobile_api, mobile_avatar_text_banner_flow):
        card_id = mobile_avatar_text_banner_flow["card_id"]
        text_value = mobile_avatar_text_banner_flow["text_value"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert text_value, "text_value empty (test_06 failed?)"

        items = wait_mobile_attr_values(
            mobile_api,
            card_id,
            expected_values=[text_value],
            attribute_id=TEXT_ATTRIBUTE_ID,
            expected_name="РњРёРЅРё СЂР°СЃСЃРєР°Р·",
            timeout_s=90,
            step_s=3,
        )
        assert items is not None, "Text attribute not found by name and value"

    @allure.title("Reuse avatar attachment as banner attachment")
    def test_08_prepare_banner_attachment(self, mobile_avatar_text_banner_flow):
        attachment_id = mobile_avatar_text_banner_flow["avatar_attachment_id"]
        assert attachment_id, "avatar_attachment_id empty (test_03 failed?)"
        mobile_avatar_text_banner_flow["banner_attachment_id"] = int(attachment_id)

    @allure.title("Merge banner attribute")
    def test_09_merge_banner(self, mobile_api, mobile_avatar_text_banner_flow):
        card_id = mobile_avatar_text_banner_flow["card_id"]
        attachment_id = mobile_avatar_text_banner_flow["banner_attachment_id"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert attachment_id, "banner_attachment_id empty (test_08 failed?)"

        banner_url = f"https://{rand_word('space', 8)}.com/{rand_word('orbit', 10)}"
        mobile_avatar_text_banner_flow["banner_url"] = banner_url

        body = build_mobile_attribute_body(
            attribute_id=BANNER_ATTRIBUTE_ID,
            name="Р‘Р°РЅРЅРµСЂ",
            sort_order=2,
            value=[banner_url],
            attachment_id=int(attachment_id),
        )
        response = merge_mobile_card_attributes(mobile_api, card_id, body)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Merge banner failed: {response.status_code}, body={response.text}"
        )

    @allure.title("085 has banner attribute")
    def test_10_attrs_have_banner(self, mobile_api, mobile_avatar_text_banner_flow):
        card_id = mobile_avatar_text_banner_flow["card_id"]
        banner_url = mobile_avatar_text_banner_flow["banner_url"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert banner_url, "banner_url empty (test_09 failed?)"

        items = wait_mobile_attr_values(
            mobile_api,
            card_id,
            expected_values=[banner_url],
            attribute_id=BANNER_ATTRIBUTE_ID,
            expected_name="Р‘Р°РЅРЅРµСЂ",
            timeout_s=180,
            step_s=3,
        )
        assert items is not None, "Banner attribute not found in 085"

    @allure.title("Delete mobile card")
    def test_11_delete_card(self, mobile_api, mobile_avatar_text_banner_flow):
        card_id = mobile_avatar_text_banner_flow["card_id"]
        assert card_id, "card_id empty (test_01 failed?)"
        response = delete_mobile_card(mobile_api, card_id)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Delete card failed: {response.status_code}, body={response.text}"
        )
        mobile_avatar_text_banner_flow["deleted"] = True
