import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_card_virtualbackgrounds.api_accounts_card_virtualbackgrounds import (
    AccountsCardVirtualBackgroundsAPI,
)
from services.accounts.accounts_card_virtualbackgrounds_add.api_accounts_card_virtualbackgrounds_add import (
    AccountsCardVirtualBackgroundsAddAPI,
)
from services.accounts.accounts_card_virtualbackgrounds_remove.api_accounts_card_virtualbackgrounds_remove import (
    AccountsCardVirtualBackgroundsRemoveAPI,
)
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.virtual_backgrounds.virtual_backgrounds_list.api_virtual_backgrounds import VirtualBackgroundsAPI


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    GET /Accounts/{account_id}/Cards/{card_id}/virtualbackground
    POST /Accounts/{account_id}/Cards/{card_id}/virtualbackground
    DELETE /Accounts/{account_id}/Cards/{card_id}/virtualbackground
    """
)
class TestAccountsCardVirtualBackgrounds:
    @allure.title("GET /Accounts/{account_id}/Cards/{card_id}/virtualbackground returns list")
    def test_accounts_card_virtualbackgrounds_200(self, cfg):
        response, model = AccountsCardVirtualBackgroundsAPI().get_accounts_card_virtualbackgrounds(
            int(cfg["lk_account_id"]),
            1,
        )

        assert response.status_code == HTTPStatus.OK
        assert isinstance(model.items, list)

    @allure.title("POST add → GET verify present → DELETE remove → GET verify absent")
    def test_accounts_card_virtualbackgrounds_add_remove_flow(self, created_card):
        card = CardByIdAPI().get_card_by_id(created_card.id)
        assert card.accountID is not None, "Card accountID is empty"
        account_id = int(card.accountID)
        card_id = int(created_card.id)

        with allure.step("GET /VirtualBackgrounds — pick first available background"):
            _, bg_model = VirtualBackgroundsAPI().get_virtual_backgrounds(offset=0, fetch=10)
            if not bg_model.items or bg_model.items[0].id is None:
                pytest.skip("No virtual backgrounds available in the system")
            background_id = int(bg_model.items[0].id)

        with allure.step(f"POST — add background id={background_id} to card"):
            AccountsCardVirtualBackgroundsAddAPI().add_accounts_card_virtualbackgrounds(
                account_id, card_id, [background_id]
            )

        with allure.step("GET — verify background is present on card"):
            _, card_bg_model = AccountsCardVirtualBackgroundsAPI().get_accounts_card_virtualbackgrounds(
                account_id, card_id
            )
            present_ids = [int(item.id) for item in card_bg_model.items if item.id is not None]
            assert background_id in present_ids, f"Background {background_id} not found after add: {present_ids}"

        with allure.step(f"DELETE — remove background id={background_id} from card"):
            AccountsCardVirtualBackgroundsRemoveAPI().remove_accounts_card_virtualbackgrounds(
                account_id, card_id, [background_id]
            )

        with allure.step("GET — verify background is absent from card"):
            _, card_bg_model_after = AccountsCardVirtualBackgroundsAPI().get_accounts_card_virtualbackgrounds(
                account_id, card_id
            )
            remaining_ids = [int(item.id) for item in card_bg_model_after.items if item.id is not None]
            assert background_id not in remaining_ids, f"Background {background_id} still present after remove"
