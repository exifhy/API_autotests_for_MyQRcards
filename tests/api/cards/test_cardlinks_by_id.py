import allure
import pytest

from services.cardlinks.cardlink_by_id.api_cardlink_by_id import CardLinkByIdAPI
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.cards_list.api_cards_list import CardsListAPI
from tests.api.cards.helpers import extract_card_link_id

_SKIP_MSG = "unbound_cardlink_id not configured"


@allure.epic("API")
@allure.feature("CardLinks")
@pytest.mark.api
@allure.description(
    """
    /cardlinks/{cardLink}
    """
)
class TestCardLinksById:
    @allure.title("GET /Cards -> GET /cardlinks/{cardLink}")
    @pytest.mark.smoke
    def test_cardlinks_by_id_flow(self):
        _, cards = CardsListAPI().get_cards(range_header=None, offset=0, fetch=20)
        assert cards.items, "Cards list is empty"

        source_card_id = next((item.id for item in cards.items if item.id is not None and item.url), None)
        assert source_card_id is not None, "No suitable card found in cards list"

        card = CardByIdAPI().get_card_by_id(source_card_id)
        assert card.url, "Card public url is empty"
        card_link_id = extract_card_link_id(card.url)

        model = CardLinkByIdAPI().get_cardlink_by_id(card_link_id)
        account_obj = getattr(model, "account", None)
        card_obj = getattr(model, "card", None)

        assert model.cardID in (None, source_card_id) or card_obj is not None or model.id is not None
        assert (
            model.accountID is not None
            or model.customCardLinkUrl is not None
            or model.name is not None
            or account_obj is not None
            or card_obj is not None
        )

    @allure.title("GET /cardlinks/{cardLink} — unbound cardlink without flag returns 204")
    @pytest.mark.smoke
    def test_cardlinks_by_id_unbound_no_flag(self, cfg):
        cardlink_id = cfg.get("unbound_cardlink_id")
        if not cardlink_id:
            pytest.skip(_SKIP_MSG)

        model = CardLinkByIdAPI().get_cardlink_by_id(cardlink_id)
        assert model is None, f"Expected 204 (None) for unbound cardlink without flag, got model: {model}"

    @allure.title("GET /cardlinks/{cardLink}?IsSkipCheck=true — unbound cardlink returns 200 with data")
    @pytest.mark.smoke
    def test_cardlinks_by_id_unbound_skip_check_true(self, cfg):
        cardlink_id = cfg.get("unbound_cardlink_id")
        if not cardlink_id:
            pytest.skip(_SKIP_MSG)

        model = CardLinkByIdAPI().get_cardlink_by_id(cardlink_id, is_skip_check=True)
        assert model is not None, "Expected 200 with data for unbound cardlink with IsSkipCheck=true"

    @allure.title("GET /cardlinks/{cardLink}?IsSkipCheck=false — unbound cardlink returns 204")
    @pytest.mark.smoke
    def test_cardlinks_by_id_unbound_skip_check_false(self, cfg):
        cardlink_id = cfg.get("unbound_cardlink_id")
        if not cardlink_id:
            pytest.skip(_SKIP_MSG)

        model = CardLinkByIdAPI().get_cardlink_by_id(cardlink_id, is_skip_check=False)
        assert model is None, f"Expected 204 (None) for unbound cardlink with IsSkipCheck=false, got model: {model}"
