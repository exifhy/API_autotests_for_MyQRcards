import allure
import pytest
from http import HTTPStatus

from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.cards_hide.api_cards_hide import CardsHideAPI
from services.cards.cards_show.api_cards_show import CardsShowAPI
from tests.api.cards.helpers import wait_card_hidden_state


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/hide и /Cards/show
    """
)
class TestCardsShowHideFlow:
    @allure.title("POST /Cards -> PUT /Cards/hide -> GET /Cards/{id} -> PUT /Cards/show -> GET /Cards/{id}")
    @pytest.mark.smoke
    def test_cards_show_hide_flow(self, created_card):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None

        item = {"AccountID": card.accountID, "CardID": created.id}

        hidden_response = CardsHideAPI().hide_cards(item)
        assert hidden_response.status_code == HTTPStatus.ACCEPTED

        hidden_card = wait_card_hidden_state(created.id, True)
        assert hidden_card is not None
        assert hidden_card.isHidden is True

        shown_response = CardsShowAPI().show_cards(item)
        assert shown_response.status_code == HTTPStatus.ACCEPTED

        visible_card = wait_card_hidden_state(created.id, False)
        assert visible_card is not None
        assert visible_card.isHidden is False
