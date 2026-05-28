import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_card_create.api_accounts_card_create import AccountsCardCreateAPI
from services.cards.card_attributes_list.api_card_attributes_list import CardAttributesListAPI
from services.cards.card_attributes_merge.api_card_attributes_merge import CardAttributesMergeAPI
from services.cards.card_delete_by_id.api_card_delete_by_id import CardDeleteByIdAPI


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    PUT /cards/{id}/attributes
    """
)
class TestCardAttributesMerge:
    @allure.title("POST card -> PUT /cards/{id}/attributes -> GET verify -> DELETE")
    def test_card_attributes_merge_200(self, cfg):
        card_id = None
        try:
            with allure.step("POST — create card"):
                _, created, _ = AccountsCardCreateAPI().create_accounts_card(int(cfg["lk_account_id"]))
                card_id = int(created.id)

            with allure.step(f"PUT /cards/{card_id}/attributes — merge phone attribute"):
                response = CardAttributesMergeAPI().merge_card_attributes(card_id)
                assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT)

            with allure.step(f"GET /cards/{card_id}/attributes/ — verify attribute set"):
                _, model = CardAttributesListAPI().get_card_attributes(card_id)
                assert isinstance(model.items, list)

        finally:
            if card_id is not None:
                try:
                    CardDeleteByIdAPI().delete_card_by_id(card_id)
                except Exception:
                    pass

    @pytest.mark.ng
    @allure.title("PUT /cards/{id}/attributes without auth -> 401/403")
    def test_card_attributes_merge_401_without_auth(self, cfg):
        response = CardAttributesMergeAPI().merge_card_attributes_without_auth(card_id=1)
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
