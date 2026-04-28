import allure
import pytest
from http import HTTPStatus

from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.card_create.api_card_create import CardCreateAPI
from services.cards.card_copy.api_card_copy import CardCopyAPI
from services.cards.card_delete_by_id.api_card_delete_by_id import CardDeleteByIdAPI
from tests.api.companies.helpers import wait_account_present_in_company


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /cards/card/copy
    """
)
class TestCardsCopyFlow:
    @allure.title("POST /Cards -> POST /cards/card/copy -> GET /Cards/v2.0 -> DELETE copied card")
    @pytest.mark.smoke
    def test_cards_copy_flow(self, cfg, created_company):
        created_card = None
        try:
            created_card = CardCreateAPI().create_card(
                subscription_id=cfg["subscription_id"],
                company_id=cfg["company_id_create"],
            )
        except AssertionError as exc:
            if "SubscriptionConstraint" in str(exc):
                pytest.skip("No available cards to create source card on current subscription")
            raise
        try:
            source_card = CardByIdAPI().get_card_by_id(created_card.id)
            assert source_card.accountID is not None
            assert source_card.name is not None and source_card.name != ""

            response, _ = CardCopyAPI().copy_cards(
                {
                    "AccountID": source_card.accountID,
                    "CardID": created_card.id,
                    "CompanyID": created_company["id"],
                },
                allow_subscription_constraint=True,
            )
            if response.status_code == HTTPStatus.FORBIDDEN and "SubscriptionConstraint" in response.text:
                pytest.skip("No available cards to copy on current subscription")
            assert response.status_code == HTTPStatus.CREATED

            ok = wait_account_present_in_company(
                source_card.accountID,
                created_company["id"],
            )
            assert ok, "Copied account/card did not appear in target company"
        finally:
            if created_card is not None:
                CardDeleteByIdAPI().delete_card_by_id(created_card.id)
