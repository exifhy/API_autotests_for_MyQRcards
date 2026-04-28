import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_card_leadgen_form_by_id.api_accounts_card_leadgen_form_by_id import (
    AccountsCardLeadGenFormByIdAPI,
)
from services.accounts.accounts_card_leadgen_forms_create.api_accounts_card_leadgen_forms_create import (
    AccountsCardLeadGenFormsCreateAPI,
)
from services.accounts.accounts_card_leadgen_forms_delete.api_accounts_card_leadgen_forms_delete import (
    AccountsCardLeadGenFormsDeleteAPI,
)
from services.accounts.accounts_card_leadgen_forms_update.api_accounts_card_leadgen_forms_update import (
    AccountsCardLeadGenFormsUpdateAPI,
)
from services.accounts.accounts_custom_message_template_by_leadgen_form.api_accounts_custom_message_template_by_leadgen_form import (
    AccountsCustomMessageTemplateByLeadGenFormAPI,
)
from services.accounts.accounts_custom_message_templates.api_accounts_custom_message_templates import (
    AccountsCustomMessageTemplatesAPI,
)
from services.accounts.accounts_custom_message_templates_create.api_accounts_custom_message_templates_create import (
    AccountsCustomMessageTemplatesCreateAPI,
)
from services.accounts.accounts_custom_message_templates_delete.api_accounts_custom_message_templates_delete import (
    AccountsCustomMessageTemplatesDeleteAPI,
)
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from src.support.waiter import wait_until


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    /Accounts/{accountID}/Cards/{cardID}/leadGenForms
    """
)
class TestAccountsCardLeadGenFormsCustomMessageTemplate:
    @allure.title("PUT leadGenForm with CustomMessageTemplateID -> GET MessageTemplate")
    @pytest.mark.smoke
    def test_accounts_card_leadgen_form_can_link_custom_message_template(
        self,
        created_card,
        leadgen_field_template_id,
    ):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        leadgen_form_id = None
        template_id = None
        try:
            created_form = AccountsCardLeadGenFormsCreateAPI().create_accounts_card_leadgen_form(
                card.accountID,
                created.id,
                field_template_id=leadgen_field_template_id,
            )
            leadgen_form_id = created_form.id
            assert leadgen_form_id is not None

            _, created_template, created_template_payload = AccountsCustomMessageTemplatesCreateAPI().create_accounts_custom_message_template(
                card.accountID
            )
            template_id = created_template.id
            assert template_id is not None

            updated_response, payload = AccountsCardLeadGenFormsUpdateAPI().update_accounts_card_leadgen_forms(
                card.accountID,
                created.id,
                leadgen_form_id=leadgen_form_id,
                field_template_id=leadgen_field_template_id,
                custom_message_template_id=template_id,
            )
            assert updated_response.status_code == HTTPStatus.ACCEPTED
            assert payload[0]["CustomMessageTemplateID"] == template_id

            updated_form = AccountsCardLeadGenFormByIdAPI().get_accounts_card_leadgen_form_by_id(
                card.accountID,
                created.id,
                leadgen_form_id,
            )
            assert updated_form.customMessageTemplateID == template_id

            linked_template = AccountsCustomMessageTemplateByLeadGenFormAPI().get_accounts_custom_message_template_by_leadgen_form(
                card.accountID,
                created.id,
                leadgen_form_id,
            )
            assert linked_template.subjectTemplate == created_template_payload["subjectTemplate"]
            assert linked_template.contentTemplate == created_template_payload["contentTemplate"]
        finally:
            if leadgen_form_id is not None:
                try:
                    AccountsCardLeadGenFormsDeleteAPI().delete_accounts_card_leadgen_forms(
                        card.accountID,
                        created.id,
                        [leadgen_form_id],
                    )
                    deleted = wait_until(
                        lambda: _leadgen_absent(card.accountID, created.id, int(leadgen_form_id)),
                        timeout_s=60,
                        step_s=3,
                    )
                    assert deleted is True, f"Leadgen form id={leadgen_form_id} still visible after delete"
                except Exception:
                    pass
            if template_id is not None:
                try:
                    AccountsCustomMessageTemplatesDeleteAPI().delete_accounts_custom_message_templates(
                        card.accountID,
                        [template_id],
                    )
                    deleted = wait_until(
                        lambda: _templates_absent(card.accountID, [int(template_id)]),
                        timeout_s=60,
                        step_s=3,
                    )
                    assert deleted is True, f"Custom message template id={template_id} still visible after delete"
                except Exception:
                    pass


def _leadgen_absent(account_id: int, card_id: int, leadgen_form_id: int) -> bool | None:
    from services.accounts.accounts_card_leadgen_forms.api_accounts_card_leadgen_forms import (
        AccountsCardLeadGenFormsAPI,
    )

    response, model = AccountsCardLeadGenFormsAPI().get_accounts_card_leadgen_forms(account_id, card_id)
    if response.status_code not in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT):
        return None
    return True if all(item.id != leadgen_form_id for item in model.items if item.id is not None) else None


def _templates_absent(account_id: int, template_ids: list[int]) -> bool | None:
    response, model = AccountsCustomMessageTemplatesAPI().get_accounts_custom_message_templates(account_id)
    if response.status_code not in (HTTPStatus.OK, HTTPStatus.NO_CONTENT):
        return None
    present_ids = {int(item.id) for item in model.items if item.id is not None}
    return True if present_ids.isdisjoint({int(template_id) for template_id in template_ids}) else None
