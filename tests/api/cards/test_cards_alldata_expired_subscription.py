import allure
import pytest

from services.cardlinks.cardlink_card.api_cardlink_card import CardLinkCardAPI
from services.cardlinks.cardlink_short_card.api_cardlink_short_card import CardLinkShortCardAPI
from services.cards.card_by_id_v2.api_card_by_id_v2 import CardByIdV2API
from src.support.token_utils import get_expired_jwt

_EXPIRED_CARD_ID = 2


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    AllData=true flag: returns expired subscription cards as 200 instead of 409.
    REQUIREMENT 30709.

    - 051 V2:  GET /cards/{id}/V2?AllData=true  — authenticated with EXPIRED_JWT
    - 090:     GET /cardLinks/{token}/card?AllData=true
    - 051.2.2: GET /cardLinks/{token}/short/card?AllData=true
    """
)
class TestCardsAllDataExpiredSubscription:
    @allure.title("GET /cards/2/V2?AllData=true — expired subscription returns 200, isValid=false")
    @pytest.mark.smoke
    def test_card_by_id_v2_alldata_expired(self):
        token = get_expired_jwt()
        if not token:
            pytest.skip("EXPIRED_JWT not configured")

        card = CardByIdV2API().get_card_by_id_v2(_EXPIRED_CARD_ID, all_data=True, token=token)
        assert card.id == _EXPIRED_CARD_ID
        assert card.subscription is not None
        assert card.subscription.isValid is False, (
            f"Expected subscription.isValid=False for expired account, got {card.subscription.isValid}"
        )
        if card.subscriptionStatus is not None:
            assert card.subscriptionStatus == "expired", (
                f"Expected subscriptionStatus='expired', got '{card.subscriptionStatus}'"
            )

    @allure.title("GET /cardLinks/{token}/card?AllData=true — expired card returns 200, isValid=false")
    @pytest.mark.smoke
    def test_cardlink_card_alldata_expired(self, cfg):
        cardlink_id = cfg.get("expired_cardlink_id")
        if not cardlink_id:
            pytest.skip("expired_cardlink_id not configured")

        card = CardLinkCardAPI().get_cardlink_card(cardlink_id, all_data=True)
        assert card.subscription is not None
        assert card.subscription.isValid is False, (
            f"Expected subscription.isValid=False for expired card, got {card.subscription.isValid}"
        )
        if card.subscriptionStatus is not None:
            assert card.subscriptionStatus == "expired", (
                f"Expected subscriptionStatus='expired', got '{card.subscriptionStatus}'"
            )

    @allure.title("GET /cardLinks/{token}/short/card?AllData=true — expired card returns isSubscriptionValid=false")
    @pytest.mark.smoke
    def test_cardlink_short_card_alldata_expired(self, cfg):
        cardlink_id = cfg.get("expired_cardlink_id")
        if not cardlink_id:
            pytest.skip("expired_cardlink_id not configured")

        card = CardLinkShortCardAPI().get_cardlink_short_card(cardlink_id, all_data=True)
        assert card.isSubscriptionValid is False, (
            f"Expected isSubscriptionValid=False, got '{card.isSubscriptionValid}'"
        )
