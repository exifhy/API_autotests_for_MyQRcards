import allure
import pytest
from http import HTTPStatus

from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.card_leadgen_forms_create.payloads import Payloads
from services.cards.card_delete_by_id.api_card_delete_by_id import CardDeleteByIdAPI
from tests.e2e.cards.helpers import create_card_and_fill_flow, wait_accounts_leadgen_form_present


@allure.epic("LK")
@allure.feature("Cards")
@allure.title("Create card -> Add leadgen form -> Verify list -> Delete")
@allure.description(
    """
    /Cards
    /Cards/{id}
    /accounts/{accountID}/cards/{cardID}/leadgenforms
    /Cards/{id}
    """
)
@pytest.mark.e2e
class TestCardCreateLeadGenFormFlow:
    @allure.title("Create card")
    def test_01_create_card(self, cfg, card_leadgen_flow):
        create_card_and_fill_flow(
            card_leadgen_flow,
            subscription_id=cfg["subscription_id"],
            company_id=cfg["company_id_create"],
        )
        assert card_leadgen_flow["card_id"], "card_id empty after create"
        assert card_leadgen_flow["account_id"], "account_id empty after create"

    @allure.title("Get created card")
    def test_02_get_created_card(self, card_leadgen_flow):
        card_id = card_leadgen_flow["card_id"]
        account_id = card_leadgen_flow["account_id"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert account_id, "account_id empty (test_01 failed?)"

        fetched = CardByIdAPI().get_card_by_id(card_id)
        assert fetched.id == card_id
        assert fetched.accountID == account_id
        assert fetched.person is not None

    @allure.title("Add leadgen form")
    def test_03_add_leadgen_form(self, lk_api, card_leadgen_flow, leadgen_field_template_id):
        card_id = card_leadgen_flow["card_id"]
        account_id = card_leadgen_flow["account_id"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert account_id, "account_id empty (test_01 failed?)"

        payload = Payloads.build_card_leadgen_form_create_payload(field_template_id=leadgen_field_template_id)
        card_leadgen_flow["leadgen_payload"] = payload

        response = lk_api.post(
            f"/accounts/{int(account_id)}/cards/{int(card_id)}/leadgenforms",
            json=payload,
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Add leadgen form failed: {response.status_code}, body={response.text}"
        )

        leadgen_form_id = response.json().get("id")
        assert leadgen_form_id, f"No leadgen form id in response: {response.text}"
        card_leadgen_flow["leadgen_form_id"] = int(leadgen_form_id)

    @allure.title("Leadgen form appears in list")
    def test_04_list_contains_leadgen_form(self, lk_api, card_leadgen_flow, leadgen_field_template_id):
        card_id = card_leadgen_flow["card_id"]
        account_id = card_leadgen_flow["account_id"]
        leadgen_form_id = card_leadgen_flow["leadgen_form_id"]
        payload = card_leadgen_flow["leadgen_payload"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert account_id, "account_id empty (test_01 failed?)"
        assert leadgen_form_id, "leadgen_form_id empty (test_03 failed?)"
        assert payload, "leadgen_payload empty (test_03 failed?)"

        found = wait_accounts_leadgen_form_present(
            lk_api,
            account_id=account_id,
            card_id=card_id,
            expected_form_text=payload["formText"],
            expected_button_text=payload["buttonText"],
            expected_field_template_id=leadgen_field_template_id,
            timeout_s=60,
            step_s=3,
        )
        assert found is not None, "Leadgen form not found in Accounts/Card leadgen list"
        assert int(found["id"]) == int(leadgen_form_id)

    @allure.title("Delete card")
    def test_05_delete_card(self, card_leadgen_flow):
        card_id = card_leadgen_flow["card_id"]
        assert card_id, "card_id empty (test_01 failed?)"

        response = CardDeleteByIdAPI().delete_card_by_id(card_id)
        assert response.status_code == HTTPStatus.ACCEPTED
        card_leadgen_flow["deleted"] = True
