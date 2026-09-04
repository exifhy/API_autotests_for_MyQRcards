import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_google_wallet.api_accounts_google_wallet import AccountsGoogleWalletAPI
from services.accounts.accounts_google_wallet_by_link.api_accounts_google_wallet_by_link import (
    AccountsGoogleWalletByLinkAPI,
)
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.card_delete_by_id.api_card_delete_by_id import CardDeleteByIdAPI
from src.support.helper import Helper
from tests.api.accounts.helpers import decode_jwt_payload
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

    @allure.title("POST /Accounts/GoogleWallet/{cardID} for nonexistent card -> 404")
    @pytest.mark.ng
    def test_google_wallet_by_card_id_nonexistent_404(self):
        # AC (REQUIREMENT 32221) says a not-found card should give "204 No Content либо принятый
        # в API код". QA reported live (work item 32221 comment, 2026-09-03) that dev originally
        # returned 403 Forbidden here — misleading, since it reads like an ownership/auth problem
        # rather than "card not found". Fixed by 2026-09-04 (re-verified live): now 404 CardNotFound,
        # which is an accepted API code per the AC wording.
        response = AccountsGoogleWalletAPI().create_google_wallet_raw(255)
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f"Expected HTTPStatus.NOT_FOUND, got {response.status_code}: {response.text}"
        )

    @allure.title("POST /Accounts/GoogleWallet/{cardID} for a deleted card -> 404")
    @pytest.mark.ng
    def test_google_wallet_by_card_id_deleted_card_404(self, created_card):
        # Same fix as test_google_wallet_by_card_id_nonexistent_404 above — QA checklist on the work
        # item marked "deleted card -> 204" as ❌ (failing, was 403) as of 2026-09-03; re-verified
        # live on 2026-09-04 after the fix landed — now 404 CardNotFound.
        card_id = created_card.id
        CardDeleteByIdAPI().delete_card_by_id(card_id)

        response = AccountsGoogleWalletAPI().create_google_wallet_raw(card_id)
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f"Expected HTTPStatus.NOT_FOUND, got {response.status_code}: {response.text}"
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

    @allure.title("Google Wallet JWT payload: header shows full name including middle name")
    def test_google_wallet_jwt_header_includes_middle_name(self, created_card):
        # AC asks for "ФИО" (full name incl. patronymic) in the Pass. QA found live (REQUIREMENT 32221
        # comment, 2026-09-03) that the middle name didn't come through — only first+last name — even
        # though the underlying card person has one. Fixed by 2026-09-04 (re-verified live): the header
        # now includes all three parts, in "firstName middleName lastName" order.
        card = CardByIdAPI().get_card_by_id(created_card.id)
        assert card.person is not None
        assert card.person.middleName, "Test card unexpectedly has no middleName — fixture data changed?"

        result = AccountsGoogleWalletAPI().create_google_wallet(created_card.id)
        assert result is not None, "Expected 200 with a body, got 204"

        payload = decode_jwt_payload(result.jwt)
        header_value = payload["payload"]["genericObjects"][0]["header"]["defaultValue"]["value"]

        expected = f"{card.person.firstName} {card.person.middleName} {card.person.lastName}"
        assert header_value == expected, f"Expected header '{expected}', got '{header_value}'"

    @allure.title("Google Wallet JWT payload: QR barcode points at the card's public link")
    def test_google_wallet_jwt_barcode_points_to_card_url(self, created_card):
        card = CardByIdAPI().get_card_by_id(created_card.id)
        assert card.url, "Card public url is empty"

        result = AccountsGoogleWalletAPI().create_google_wallet(created_card.id)
        assert result is not None, "Expected 200 with a body, got 204"

        payload = decode_jwt_payload(result.jwt)
        generic_object = payload["payload"]["genericObjects"][0]
        barcode = generic_object["barcode"]

        assert barcode["type"] == "QR_CODE"
        assert barcode["value"] == card.url
        assert generic_object["linksModuleData"]["uris"][0]["uri"] == card.url

    @allure.title("Google Wallet JWT payload: logo image URL is reachable")
    def test_google_wallet_jwt_logo_url_reachable(self, created_card):
        # QA reported a visually broken/oversized logo in the actual Google Wallet app (REQUIREMENT
        # 32221 comment, 2026-09-03). We can't verify rendering via API, but we can at least confirm
        # the logo URL embedded in the JWT actually resolves to an image — a broken/404 URL would be
        # a stronger, API-testable version of the same symptom.
        result = AccountsGoogleWalletAPI().create_google_wallet(created_card.id)
        assert result is not None, "Expected 200 with a body, got 204"

        payload = decode_jwt_payload(result.jwt)
        logo_uri = payload["payload"]["genericObjects"][0]["logo"]["sourceUri"]["uri"]
        assert logo_uri, "logo.sourceUri.uri is empty in the Wallet payload"

        response = Helper()._call("GET", logo_uri)
        assert response.status_code == HTTPStatus.OK, (
            f"Logo URL is not reachable: {response.status_code} {logo_uri}"
        )
        content_type = response.headers.get("Content-Type", "")
        assert content_type.startswith("image/"), f"Expected an image Content-Type, got '{content_type}'"
