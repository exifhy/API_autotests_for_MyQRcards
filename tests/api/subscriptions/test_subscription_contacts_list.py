import allure
import pytest
from http import HTTPStatus

from services.subscriptions.subscription_contacts_list.api_subscription_contacts_list import (
    SubscriptionContactsListAPI,
)


@allure.epic("API")
@allure.feature("Subscriptions")
@pytest.mark.api
@allure.description(
    """
    GET /Subscriptions/{id}/contacts
    """
)
class TestSubscriptionContactsList:
    @allure.title("GET /Subscriptions/{id}/contacts")
    @pytest.mark.smoke
    def test_subscription_contacts_list_200(self, cfg):
        sub_id = cfg.get("subscription_id")
        assert sub_id, "cfg['subscription_id'] is empty"

        response, model = SubscriptionContactsListAPI().get_subscription_contacts(
            int(sub_id), account_id=int(cfg["lk_account_id"])
        )

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
        assert isinstance(model.items, list)

    @pytest.mark.ng
    @allure.title("GET /Subscriptions/{id}/contacts without auth -> 401/403")
    def test_subscription_contacts_list_401_without_auth(self, cfg):
        sub_id = cfg.get("subscription_id")
        assert sub_id, "cfg['subscription_id'] is empty"

        response = SubscriptionContactsListAPI().get_subscription_contacts_without_auth(
            int(sub_id), account_id=int(cfg["lk_account_id"])
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
