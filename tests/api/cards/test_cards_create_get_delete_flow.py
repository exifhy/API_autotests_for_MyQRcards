import allure
import pytest
from http import HTTPStatus

from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.card_create.api_card_create import CardCreateAPI
from services.cards.card_delete_by_id.api_card_delete_by_id import CardDeleteByIdAPI
from tests.api.cards.helpers import assert_card_full


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards
    """
)
class TestCardsCreateGetDeleteFlow:
    @allure.title("POST /Cards -> GET /Cards/{id} -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_cards_create_get_delete_flow(self, cfg):
        created = None
        try:
            created = CardCreateAPI().create_card(
                subscription_id=cfg['subscription_id'],
                company_id=cfg['company_id_create'],
            )
            assert created.id is not None

            fetched = CardByIdAPI().get_card_by_id(created.id)
            assert_card_full(fetched, card_id=created.id)

            deleted = CardDeleteByIdAPI().delete_card_by_id(created.id)
            assert deleted.status_code == HTTPStatus.ACCEPTED
            created = None
        finally:
            if created is not None:
                try:
                    CardDeleteByIdAPI().delete_card_by_id(created.id)
                except Exception:
                    pass
