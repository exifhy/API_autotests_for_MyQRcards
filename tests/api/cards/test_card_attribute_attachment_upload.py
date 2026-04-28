import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_card_create.api_accounts_card_create import AccountsCardCreateAPI
from services.cards.card_attributes_merge.api_card_attributes_merge import CardAttributesMergeAPI
from services.cards.card_attributes_list.api_card_attributes_list import CardAttributesListAPI
from services.cards.card_attribute_attachment_upload.api_card_attribute_attachment_upload import (
    CardAttributeAttachmentUploadAPI,
)
from services.cards.card_delete_by_id.api_card_delete_by_id import CardDeleteByIdAPI
from src.constants.attributes import FILE_ATTRIBUTE_ID


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    PUT /cards/{id}/upload/fromForm
    """
)
class TestCardAttributeAttachmentUpload:
    @allure.title("POST card -> PUT attrs -> GET attrs -> PUT /cards/{id}/upload/fromForm -> DELETE")
    @pytest.mark.smoke
    def test_card_attribute_attachment_upload_200(self, cfg):
        card_id = None
        try:
            with allure.step("POST — create card"):
                _, created, _ = AccountsCardCreateAPI().create_accounts_card(int(cfg["lk_account_id"]))
                card_id = int(created.id)

            with allure.step(f"PUT /cards/{card_id}/attributes — merge file attribute"):
                merge_payload = [
                    {
                        "AttributeID": FILE_ATTRIBUTE_ID,
                        "Name": "File",
                        "SortOrder": 1,
                        "Value": [],
                        "IsEnabled": True,
                        "AttributeFormID": None,
                    }
                ]
                CardAttributesMergeAPI().merge_card_attributes(card_id, payload=merge_payload)

            with allure.step(f"GET /cards/{card_id}/attributes — find cardAttribute record id"):
                _, attrs_model = CardAttributesListAPI().get_card_attributes(card_id)
                card_attribute_id = None
                for item in attrs_model.items:
                    extra = item.model_extra or {}
                    nested = extra.get("cardAttribute") or {}
                    if isinstance(nested, dict) and nested.get("id") is not None:
                        card_attribute_id = int(nested["id"])
                        break
                assert card_attribute_id is not None, "Could not find cardAttribute.id in card attributes"

            with allure.step(f"PUT /cards/{card_id}/upload/fromForm — upload file"):
                response, model = CardAttributeAttachmentUploadAPI().upload_card_attribute_attachment(
                    card_id,
                    card_attribute_id,
                    attribute_id=FILE_ATTRIBUTE_ID,
                )

            assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.NO_CONTENT)

        finally:
            if card_id is not None:
                try:
                    CardDeleteByIdAPI().delete_card_by_id(card_id)
                except Exception:
                    pass

    @pytest.mark.ng
    @allure.title("PUT /cards/{id}/upload/fromForm without auth -> 401/403")
    def test_card_attribute_attachment_upload_401_without_auth(self, created_card):
        response = CardAttributeAttachmentUploadAPI().upload_card_attribute_attachment_without_auth(created_card.id)
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
