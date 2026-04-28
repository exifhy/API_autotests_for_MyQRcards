import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_card_create.api_accounts_card_create import AccountsCardCreateAPI
from services.cards.card_attributes_merge.api_card_attributes_merge import CardAttributesMergeAPI
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.card_delete_by_id.api_card_delete_by_id import CardDeleteByIdAPI
from services.cards.card_link_attribute_counter.api_card_link_attribute_counter import (
    CardLinkAttributeCounterAPI,
)
from src.constants.attributes import WHATSAPP_ATTRIBUTE_ID
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    205 PUT /cards/{token}/cardLink/attributes/click
    Flow: POST card -> merge WhatsApp attr -> get cardAttribute.id -> PUT click -> DELETE card
    """
)
class TestCardLinkAttributeCounter:
    @allure.title(
        "205 POST card -> PUT merge WhatsApp -> GET attrs -> PUT /cardLink/attributes/click -> DELETE card"
    )
    def test_card_link_attribute_counter_flow(self, cfg):
        card_id = None
        try:
            with allure.step("POST — create card"):
                _, created, _ = AccountsCardCreateAPI().create_accounts_card(int(cfg["lk_account_id"]))
                card_id = int(created.id)

            with allure.step(f"GET /cards/{card_id} — extract cardlink token"):
                card = CardByIdAPI().get_card_by_id(card_id)
                assert card.url, "Card url is empty — no cardlink token"
                token = extract_card_link_id(card.url)

            with allure.step(f"PUT /cards/{card_id}/attributes — merge WhatsApp attribute"):
                merge_payload = [
                    {
                        "AttributeID": WHATSAPP_ATTRIBUTE_ID,
                        "Name": "WhatsApp",
                        "SortOrder": 1,
                        "Value": ["+79000000001"],
                        "IsEnabled": True,
                        "AttributeFormID": None,
                    }
                ]
                CardAttributesMergeAPI().merge_card_attributes(card_id, payload=merge_payload)

            with allure.step(f"205 PUT /cards/{token}/cardLink/attributes/click"):
                response = CardLinkAttributeCounterAPI().add_attribute_click(
                    token,
                    {"AttributeID": WHATSAPP_ATTRIBUTE_ID, "CardAttributeID": 1},
                )
                assert response.status_code in (
                    HTTPStatus.OK,
                    HTTPStatus.ACCEPTED,
                    HTTPStatus.NO_CONTENT,
                )

        finally:
            if card_id is not None:
                try:
                    CardDeleteByIdAPI().delete_card_by_id(card_id)
                except Exception:
                    pass
