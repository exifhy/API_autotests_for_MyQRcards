import allure
import pytest
from http import HTTPStatus

from src.constants.attributes import AVATAR_ATTRIBUTE_ID_V2, PHOTO_GALLERY_ATTRIBUTE_ID
from src.resources.mobile_api import (
    delete_mobile_card,
    list_mobile_card_attributes,
    merge_mobile_card_attributes,
    update_mobile_card_v2,
    upload_mobile_attachment_v2,
)
from tests.e2e.mobile.builders import build_mobile_update_payload
from tests.e2e.mobile.helpers import (
    extract_mobile_attachment_id,
    wait_mobile_attr_values,
    wait_mobile_gallery_contains,
    wait_mobile_card_ready,
)


@allure.epic("Mobile APP")
@allure.feature("Cards")
@allure.title("Create card -> Upload avatar and photo gallery -> Delete")
@pytest.mark.mobile
@pytest.mark.e2e
class TestMobileAppCardUploadAvatarAndPhoto:
    @allure.title("Create mobile card")
    def test_01_create_card(self, mobile_api, mobile_avatar_photo_flow):
        response = mobile_api.post("/cards/V2.0", json=mobile_avatar_photo_flow["payload"])
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
            f"Create card failed: {response.status_code}, body={response.text}"
        )
        card_id = response.json().get("id")
        assert card_id, f"No card id in response: {response.text}"
        mobile_avatar_photo_flow["card_id"] = int(card_id)

    @allure.title("Get card after create")
    def test_02_get_card_after_create(self, mobile_api, mobile_avatar_photo_flow):
        card_id = mobile_avatar_photo_flow["card_id"]
        assert card_id, "card_id empty (test_01 failed?)"
        response = wait_mobile_card_ready(mobile_api, card_id)
        assert response.status_code == HTTPStatus.OK, (
            f"GET card failed: {response.status_code}, body={response.text}"
        )

    @allure.title("Upload 5 photos as avatar attachments")
    def test_03_upload_photos(self, mobile_api, mobile_avatar_photo_flow):
        uploaded_ids = []
        for file_path in mobile_avatar_photo_flow["media"]["photo_paths"]:
            response = upload_mobile_attachment_v2(
                mobile_api,
                file_path=file_path,
                attribute_id=AVATAR_ATTRIBUTE_ID_V2,
            )
            assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED), (
                f"Upload photo failed: {response.status_code}, body={response.text}"
            )
            uploaded_ids.append(extract_mobile_attachment_id(response))

        mobile_avatar_photo_flow["uploaded_ids"] = uploaded_ids

    @allure.title("Update card avatar gallery")
    def test_04_update_card_set_avatar_gallery(self, mobile_api, mobile_avatar_photo_flow):
        card_id = mobile_avatar_photo_flow["card_id"]
        uploaded_ids = mobile_avatar_photo_flow["uploaded_ids"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert len(uploaded_ids) == 5, f"Expected 5 uploaded ids, got {len(uploaded_ids)}"

        payload = build_mobile_update_payload(
            attachment_ids=uploaded_ids,
            name="TestUpd",
        )

        response = update_mobile_card_v2(mobile_api, card_id, payload)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Update card failed: {response.status_code}, body={response.text}"
        )

    @allure.title("Get card contains gallery ids")
    def test_05_get_card_contains_gallery_ids(self, mobile_api, mobile_avatar_photo_flow):
        card_id = mobile_avatar_photo_flow["card_id"]
        expected_ids = mobile_avatar_photo_flow["uploaded_ids"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert expected_ids, "uploaded_ids empty (test_03 failed?)"

        card_json = wait_mobile_gallery_contains(
            mobile_api,
            card_id,
            expected_ids,
            timeout_s=60,
            step_s=3,
        )
        assert card_json is not None, f"Gallery does not contain uploaded ids: {expected_ids}"

    @allure.title("Merge photo gallery attribute")
    def test_06_merge_photo_gallery_attr(self, mobile_api, mobile_avatar_photo_flow):
        card_id = mobile_avatar_photo_flow["card_id"]
        uploaded_ids = mobile_avatar_photo_flow["uploaded_ids"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert uploaded_ids, "uploaded_ids empty (test_03 failed?)"

        body = [
            {
                "AttributeID": PHOTO_GALLERY_ATTRIBUTE_ID,
                "Name": "Фотогалерея",
                "SortOrder": 3,
                "Value": [int(item) for item in uploaded_ids],
                "IsEnabled": True,
            }
        ]
        response = merge_mobile_card_attributes(mobile_api, card_id, body)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Merge photo gallery failed: {response.status_code}, body={response.text}"
        )

    @allure.title("Attributes list has photo gallery values")
    def test_07_attrs_have_photo_gallery(self, mobile_api, mobile_avatar_photo_flow):
        card_id = mobile_avatar_photo_flow["card_id"]
        expected_ids = [str(item) for item in mobile_avatar_photo_flow["uploaded_ids"]]
        assert card_id, "card_id empty (test_01 failed?)"
        assert expected_ids, "uploaded_ids empty (test_03 failed?)"

        items = wait_mobile_attr_values(
            mobile_api,
            card_id,
            expected_values=expected_ids,
            attribute_id=PHOTO_GALLERY_ATTRIBUTE_ID,
            expected_name="Фотогалерея",
            timeout_s=60,
            step_s=3,
        )
        assert items is not None, f"Photo gallery values not found in 085: {expected_ids}"

    @allure.title("Delete mobile card")
    def test_08_delete_card(self, mobile_api, mobile_avatar_photo_flow):
        card_id = mobile_avatar_photo_flow["card_id"]
        assert card_id, "card_id empty (test_01 failed?)"
        response = delete_mobile_card(mobile_api, card_id)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Delete card failed: {response.status_code}, body={response.text}"
        )
        mobile_avatar_photo_flow["deleted"] = True
