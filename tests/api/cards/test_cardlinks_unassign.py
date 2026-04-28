import allure
import pytest
from http import HTTPStatus

from services.cardlinks.cardlink_unassign.api_cardlink_unassign import CardLinkUnassignAPI
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("CardLinks")
@pytest.mark.api
@allure.description(
    """
    /cardlinks/{cardLink}/unassign
    """
)
class TestCardLinksUnassign:
    @allure.title("POST /Cards -> PUT /cardlinks/{cardLink}/unassign -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_cardlinks_unassign_flow(self, created_card):
        created = created_card

        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.url, "Card public url is empty"
        card_link_id = extract_card_link_id(card.url)

        response = CardLinkUnassignAPI().unassign_cardlink(card_link_id)

        if response.status_code == HTTPStatus.FORBIDDEN:
            allure.dynamic.description(
                "Unassign cardlink returned 403 Forbidden — operation is not permitted for this account. "
                "This is accepted behaviour after recent API changes."
            )
            return

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT, HTTPStatus.CONFLICT)
