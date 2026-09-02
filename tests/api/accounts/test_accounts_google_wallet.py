import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_google_wallet.api_accounts_google_wallet import AccountsGoogleWalletAPI
from services.accounts.accounts_google_wallet_by_link.api_accounts_google_wallet_by_link import (
    AccountsGoogleWalletByLinkAPI,
)
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.card_delete_by_id.api_card_delete_by_id import CardDeleteByIdAPI
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@allure.description(
    """
    POST /Accounts/GoogleWallet/{cardID} и POST /Accounts/GoogleWallet/{cardLinkID}/card (REQUIREMENT 32221)
    """
)
class TestAccountsGoogleWallet:
    @allure.title("POST /Accounts/GoogleWallet/{cardID} for own card -> 200 + {jwt, saveUrl}")
    @pytest.mark.smoke
    def test_google_wallet_by_card_id_smoke(self, created_card):
        result = AccountsGoogleWalletAPI().create_google_wallet(created_card.id)

        assert result is not None, "Expected 200 with a body, got 204"
        assert result.jwt, "jwt is empty"
        assert result.saveUrl, "saveUrl is empty"
        assert result.saveUrl.startswith("https://pay.google.com/gp/v/save/")
        assert result.saveUrl.endswith(result.jwt)

    @allure.title("POST /Accounts/GoogleWallet/{cardLinkID}/card (public) -> 200 + {jwt, saveUrl}")
    @pytest.mark.smoke
    def test_google_wallet_by_link_smoke(self, created_card):
        card = CardByIdAPI().get_card_by_id(created_card.id)
        assert card.url, "Card public url is empty"
        card_link = extract_card_link_id(card.url)

        result = AccountsGoogleWalletByLinkAPI().create_google_wallet_by_link(card_link)

        assert result is not None, "Expected 200 with a body, got 204"
        assert result.jwt, "jwt is empty"
        assert result.saveUrl, "saveUrl is empty"
        assert result.saveUrl.startswith("https://pay.google.com/gp/v/save/")

    @allure.title("POST /Accounts/GoogleWallet/{cardID} called twice -> both calls 200 (fresh snapshot each time)")
    def test_google_wallet_by_card_id_repeated_calls(self, created_card):
        first = AccountsGoogleWalletAPI().create_google_wallet(created_card.id)
        second = AccountsGoogleWalletAPI().create_google_wallet(created_card.id)

        assert first is not None and second is not None
        assert first.jwt and second.jwt
        # Not asserting jwt1 != jwt2 here: the pass id embeds a unix-second timestamp (per API docstring),
        # so two calls within the same second can legitimately mint the same snapshot id — asserting
        # inequality would make this test flaky depending on timing.

    @allure.title("POST /Accounts/GoogleWallet/{cardID} without auth -> 401")
    @pytest.mark.ng
    def test_google_wallet_by_card_id_without_auth_401(self, created_card):
        response = AccountsGoogleWalletAPI().create_google_wallet_without_auth(created_card.id)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f"Expected HTTPStatus.UNAUTHORIZED, got {response.status_code}: {response.text}"
        )

    @allure.title("POST /Accounts/GoogleWallet/{cardID} for nonexistent card -> 403")
    @pytest.mark.ng
    def test_google_wallet_by_card_id_nonexistent_403(self):
        # Observed live on dev: nonexistent/foreign cardID gives 403 Forbidden, not 404 —
        # matches the [ProducesResponseType(Forbidden)] declared on the controller action.
        response = AccountsGoogleWalletAPI().create_google_wallet_raw(255)
        assert response.status_code == HTTPStatus.FORBIDDEN, (
            f"Expected HTTPStatus.FORBIDDEN, got {response.status_code}: {response.text}"
        )

    @allure.title("POST /Accounts/GoogleWallet/{cardID} for a deleted card -> 403")
    @pytest.mark.ng
    def test_google_wallet_by_card_id_deleted_card_403(self, created_card):
        card_id = created_card.id
        CardDeleteByIdAPI().delete_card_by_id(card_id)

        response = AccountsGoogleWalletAPI().create_google_wallet_raw(card_id)
        assert response.status_code == HTTPStatus.FORBIDDEN, (
            f"Expected HTTPStatus.FORBIDDEN, got {response.status_code}: {response.text}"
        )

    @allure.title("POST /Accounts/GoogleWallet/{cardLinkID}/card for an invalid token -> 409")
    @pytest.mark.ng
    def test_google_wallet_by_link_invalid_token_409(self):
        # Same "fake cardlink token validated before anything else" pattern already documented
        # for GET /cardlinks/{token}/catalog/{id} in docs/SERVICES.md.
        response = AccountsGoogleWalletByLinkAPI().create_google_wallet_by_link_raw("fake-token-does-not-exist")
        assert response.status_code == HTTPStatus.CONFLICT, (
            f"Expected HTTPStatus.CONFLICT, got {response.status_code}: {response.text}"
        )

    @allure.title("POST /Accounts/GoogleWallet/{cardLinkID}/card for a deleted card's link -> 409")
    @pytest.mark.ng
    def test_google_wallet_by_link_deleted_card_409(self, created_card):
        card = CardByIdAPI().get_card_by_id(created_card.id)
        card_link = extract_card_link_id(card.url)

        CardDeleteByIdAPI().delete_card_by_id(created_card.id)

        response = AccountsGoogleWalletByLinkAPI().create_google_wallet_by_link_raw(card_link)
        assert response.status_code == HTTPStatus.CONFLICT, (
            f"Expected HTTPStatus.CONFLICT, got {response.status_code}: {response.text}"
        )
