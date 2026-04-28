import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_contacts.api_accounts_contacts import AccountsContactsAPI
from src.api.endpoints import ACCOUNTS_CONTACTS_PATH_S
from src.api.lk_client import LkApiClient


@allure.epic("API")
@allure.feature("Accounts")
@allure.title("GET /accounts/contacts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    /accounts/contacts
    """
)
class TestAccountsContacts:
    @allure.title("GET /accounts/contacts → 200/206, validate response structure")
    @pytest.mark.smoke
    def test_get_contacts_200_or_206(self):
        response = AccountsContactsAPI().get_contacts()

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)

        data = response.json() if response.text else None
        assert isinstance(data, list), f"Expected list, got: {type(data)}. Body: {response.text}"

        if data:
            item = data[0]
            assert isinstance(item, dict), f"Expected dict item, got: {type(item)}"
            expected_keys = {
                "firstName",
                "lastName",
                "email",
                "mobilePhone",
                "companyName",
                "position",
                "created",
                "accountID",
                "contactID",
            }
            assert expected_keys.intersection(item.keys()), (
                f"No expected keys found in item: {item.keys()}"
            )

        if response.status_code == HTTPStatus.PARTIAL_CONTENT:
            content_range = response.headers.get("Content-Range") or response.headers.get("content-range")
            assert content_range, "206 returned but Content-Range header is missing"

    @allure.title("GET /accounts/contacts with searchText filter → 200/206")
    @pytest.mark.smoke
    def test_get_contacts_with_search_text_filters(self):
        response = AccountsContactsAPI().get_contacts(params={"searchText": "a"})

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        data = response.json() if response.text else None
        assert isinstance(data, list), f"Expected list, got: {type(data)}. Body: {response.text}"

    @allure.title("GET /accounts/contacts without auth → 401/403")
    @pytest.mark.ng
    def test_get_contacts_401_without_auth(self, cfg):
        api = LkApiClient(host=cfg["host"], token="")

        with allure.step(f"GET {ACCOUNTS_CONTACTS_PATH_S} without auth"):
            response = api.get(ACCOUNTS_CONTACTS_PATH_S)

        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
