import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_card_leadgen_form_by_id.api_accounts_card_leadgen_form_by_id import (
    AccountsCardLeadGenFormByIdAPI,
)
from services.accounts.accounts_card_leadgen_forms_create.api_accounts_card_leadgen_forms_create import (
    AccountsCardLeadGenFormsCreateAPI,
)
from services.accounts.accounts_card_leadgen_forms_update.api_accounts_card_leadgen_forms_update import (
    AccountsCardLeadGenFormsUpdateAPI,
)
from services.accounts.accounts_custom_message_template_by_leadgen_form.api_accounts_custom_message_template_by_leadgen_form import (
    AccountsCustomMessageTemplateByLeadGenFormAPI,
)
from services.accounts.accounts_custom_message_templates_create.api_accounts_custom_message_templates_create import (
    AccountsCustomMessageTemplatesCreateAPI,
)
from services.cards.card_delete_by_id.api_card_delete_by_id import CardDeleteByIdAPI
from tests.e2e.cards.helpers import create_card_and_fill_flow


@allure.epic("LK")
@allure.feature("Cards")
@allure.title("Create card -> Add leadgen form with custom message template -> Verify -> Delete")
@allure.description(
    """
    /Cards
    /accounts/{accountID}/CustomMessageTemplates
    /accounts/{accountID}/cards/{cardID}/leadgenforms
    /accounts/{accountID}/cards/{cardID}/LeadGenForms/{leadgenFormID}/MessageTemplate
    /Cards/{id}
    """
)
@pytest.mark.e2e
class TestCardCreateLeadGenFormCustomMessageFlow:
    @allure.title("Create card")
    def test_01_create_card(self, cfg, card_leadgen_message_flow):
        create_card_and_fill_flow(
            card_leadgen_message_flow,
            subscription_id=cfg["subscription_id"],
            company_id=cfg["company_id_create"],
        )
        assert card_leadgen_message_flow["card_id"], "card_id empty after create"
        assert card_leadgen_message_flow["account_id"], "account_id empty after create"

    @allure.title("Create custom message template")
    def test_02_create_custom_message_template(self, card_leadgen_message_flow):
        account_id = card_leadgen_message_flow["account_id"]
        assert account_id, "account_id empty (test_01 failed?)"

        _, created_template, payload = AccountsCustomMessageTemplatesCreateAPI().create_accounts_custom_message_template(
            account_id
        )
        assert created_template.id is not None, "Custom message template id is empty"
        card_leadgen_message_flow["template_ids"].append(int(created_template.id))
        card_leadgen_message_flow["template_payload"] = payload

    @allure.title("Create leadgen form linked with custom message template")
    def test_03_create_leadgen_form(self, card_leadgen_message_flow, leadgen_field_template_id):
        card_id = card_leadgen_message_flow["card_id"]
        account_id = card_leadgen_message_flow["account_id"]
        template_ids = card_leadgen_message_flow["template_ids"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert account_id, "account_id empty (test_01 failed?)"
        assert template_ids, "template_ids empty (test_02 failed?)"

        created_form = AccountsCardLeadGenFormsCreateAPI().create_accounts_card_leadgen_form(
            account_id,
            card_id,
            field_template_id=leadgen_field_template_id,
        )
        assert created_form.id is not None, "leadgen_form_id empty after create"
        card_leadgen_message_flow["leadgen_form_id"] = int(created_form.id)

        updated_response, payload = AccountsCardLeadGenFormsUpdateAPI().update_accounts_card_leadgen_forms(
            account_id,
            card_id,
            leadgen_form_id=card_leadgen_message_flow["leadgen_form_id"],
            field_template_id=leadgen_field_template_id,
            custom_message_template_id=template_ids[0],
        )
        assert updated_response.status_code == HTTPStatus.ACCEPTED
        assert payload[0]["CustomMessageTemplateID"] == template_ids[0]

    @allure.title("Leadgen form contains custom message template")
    def test_04_verify_linked_custom_message_template(self, card_leadgen_message_flow):
        card_id = card_leadgen_message_flow["card_id"]
        account_id = card_leadgen_message_flow["account_id"]
        leadgen_form_id = card_leadgen_message_flow["leadgen_form_id"]
        template_ids = card_leadgen_message_flow["template_ids"]
        template_payload = card_leadgen_message_flow["template_payload"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert account_id, "account_id empty (test_01 failed?)"
        assert leadgen_form_id, "leadgen_form_id empty (test_03 failed?)"
        assert template_ids, "template_ids empty (test_02 failed?)"
        assert template_payload, "template_payload empty (test_02 failed?)"

        fetched_form = AccountsCardLeadGenFormByIdAPI().get_accounts_card_leadgen_form_by_id(
            account_id,
            card_id,
            leadgen_form_id,
        )
        assert fetched_form.customMessageTemplateID == template_ids[0]

        linked_template = AccountsCustomMessageTemplateByLeadGenFormAPI().get_accounts_custom_message_template_by_leadgen_form(
            account_id,
            card_id,
            leadgen_form_id,
        )
        assert linked_template.subjectTemplate == template_payload["subjectTemplate"]
        assert linked_template.contentTemplate == template_payload["contentTemplate"]

    @allure.title("Delete card")
    def test_05_delete_card(self, card_leadgen_message_flow):
        card_id = card_leadgen_message_flow["card_id"]
        assert card_id, "card_id empty (test_01 failed?)"

        response = CardDeleteByIdAPI().delete_card_by_id(card_id)
        assert response.status_code == HTTPStatus.ACCEPTED
        card_leadgen_message_flow["deleted"] = True
