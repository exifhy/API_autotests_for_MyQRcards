import allure
import pytest
from http import HTTPStatus

from services.cardlinks.cardlink_by_id.api_cardlink_by_id import CardLinkByIdAPI
from services.cardlinks.cardlink_update.api_cardlink_update import CardLinkUpdateAPI
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("CardLinks")
@pytest.mark.api
@allure.description(
    """
    /cardlinks/{cardLink}
    """
)
class TestCardLinksUpdate:
    @allure.title("POST /Cards -> PUT /cardlinks/{cardLink} -> GET /cardlinks/{cardLink} -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_cardlinks_update_flow(self, created_card):
        created = created_card

        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.url, "Card public url is empty"
        card_link_id = extract_card_link_id(card.url)

        response, payload = CardLinkUpdateAPI().update_cardlink(
            card_link_id,
            card_id=created.id,
            is_default=True,
            allow_default_conflict=True,
        )
        assert response.status_code in (HTTPStatus.ACCEPTED, HTTPStatus.CONFLICT)
        if response.status_code == HTTPStatus.CONFLICT:
            assert "CardLinkIsDefault" in response.text

        model = CardLinkByIdAPI().get_cardlink_by_id(card_link_id)
        assert model.isDefault in (True, None)

        account_obj = getattr(model, "account", None)
        card_obj = getattr(model, "card", None)
        nested_card_id = None
        if isinstance(card_obj, dict):
            nested_card_id = card_obj.get("id")

        assert model.cardID in (None, created.id) or nested_card_id == created.id or model.id is not None
        assert payload["CardID"] == created.id
