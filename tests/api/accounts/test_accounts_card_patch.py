import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_card_patch.api_accounts_card_patch import AccountsCardPatchAPI
from services.cards.card_by_id.api_card_by_id import CardByIdAPI


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    PATCH /Accounts/{accountID}/Cards/{cardID}
    Body: [{"Field": "CompanyID", "Value": <company_id>}]
    V1 supports only CompanyID (move card to company).
    """
)
class TestAccountsCardPatch:
    @allure.title("PATCH /Accounts/{accountID}/Cards/{cardID} — move card to same company (no-op) → 200/202/204")
    def test_accounts_card_patch_company(self, created_card, cfg):
        card = CardByIdAPI().get_card_by_id(created_card.id)
        assert card.accountID is not None, "Card accountID is empty"

        response = AccountsCardPatchAPI().patch_accounts_card(
            int(card.accountID),
            int(created_card.id),
            [{"Field": "CompanyID", "Value": int(cfg["company_id_create"])}],
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT)
