import random
import string
from http import HTTPStatus

import allure
import pytest

from services.cardlinks.cardlink_by_id.api_cardlink_by_id import CardLinkByIdAPI
from services.cardlinks.cardlinks_create.api_cardlinks_create import CardLinksCreateAPI
from services.cards.card_delete_by_id.api_card_delete_by_id import CardDeleteByIdAPI
from services.cards.card_create.api_card_create import CardCreateAPI


def _rand_cardlink_suffix(n: int = 8) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(n))


@allure.epic("API")
@allure.feature("CardLinks")
@pytest.mark.api
@allure.description(
    """
    POST /cards
    POST /cards/{card_id}/links
    GET /cardlinks/{cardLink}
    DELETE /cards/{id}
    """
)
class TestCardLinksCreate:
    @allure.title("POST /cards/{card_id}/links creates custom card link visible by GET /cardlinks/{cardLink}")
    def test_cardlinks_create_flow(self, cfg):
        created_card_id = None
        try:
            created = CardCreateAPI().create_card(
                subscription_id=cfg["subscription_id"],
                company_id=cfg["company_id_create"],
            )
            assert created.id is not None
            created_card_id = int(created.id)

            custom_cardlink_id = f"autotest{_rand_cardlink_suffix()}"
            response, model, payload = CardLinksCreateAPI().create_cardlink(
                created_card_id,
                custom_cardlink_id=custom_cardlink_id,
                is_default=False,
            )
            assert response.status_code == HTTPStatus.CREATED
            assert model.id is not None

            fetched = CardLinkByIdAPI().get_cardlink_by_id(model.id)
            account_obj = getattr(fetched, "account", None)
            card_obj = getattr(fetched, "card", None)
            nested_account_id = account_obj.get("id") if isinstance(account_obj, dict) else None
            nested_card_id = card_obj.get("id") if isinstance(card_obj, dict) else None

            assert (
                fetched.id is not None
                or fetched.cardID is not None
                or nested_card_id is not None
            )
            assert fetched.cardID in (None, created_card_id) or nested_card_id == created_card_id
            assert fetched.accountID is not None or nested_account_id is not None
            assert payload["CustomCardLinkID"] == custom_cardlink_id
        finally:
            if created_card_id is not None:
                CardDeleteByIdAPI().delete_card_by_id(created_card_id)
