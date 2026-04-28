import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_cardlinks_list.api_accounts_cardlinks_list import AccountsCardLinksListAPI
from services.proxy.proxy_card_cardlink.api_proxy_card_cardlink import ProxyCardCardLinkAPI
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("Proxy")
@pytest.mark.api
@pytest.mark.smoke
@allure.description(
    """
    GET /proxy/card/cardlink/{token}
    """
)
class TestProxyCardCardLink:
    @allure.title("GET /Accounts/{id}/Cards/links -> GET /proxy/card/cardlink/{token}")
    def test_proxy_card_cardlink_200(self, cfg):
        with allure.step(f"GET cardlinks list for account {cfg['lk_account_id']}"):
            _, cardlinks = AccountsCardLinksListAPI().get_accounts_cardlinks(int(cfg["lk_account_id"]))

        assert cardlinks.items, "No cardlinks found for account — cannot test proxy endpoint"

        cardlink_url = next(
            (item.url for item in cardlinks.items if item.url),
            None,
        )
        assert cardlink_url, "No cardlink with url found"

        token = extract_card_link_id(cardlink_url)
        assert token, f"Could not extract token from url: {cardlink_url}"

        with allure.step(f"GET /proxy/card/cardlink/{token}"):
            response = ProxyCardCardLinkAPI().get_proxy_card_cardlink(token)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
