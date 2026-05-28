import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_custom_message_templates_create.api_accounts_custom_message_templates_create import (
    AccountsCustomMessageTemplatesCreateAPI,
)
from services.accounts.accounts_custom_message_templates_delete.api_accounts_custom_message_templates_delete import (
    AccountsCustomMessageTemplatesDeleteAPI,
)
from services.accounts.accounts_custom_message_templates.api_accounts_custom_message_templates import (
    AccountsCustomMessageTemplatesAPI,
)
from services.cards.card_leadgen_form_by_id.api_card_leadgen_form_by_id import (
    CardLeadGenFormByIdAPI,
)
from services.cards.card_leadgen_forms_update.api_card_leadgen_forms_update import (
    CardLeadGenFormsUpdateAPI,
)
from tests.api.cards.helpers import (
    create_card_leadgen_form,
    delete_card_leadgen_form_best_effort,
    get_card_account_id,
)
from src.support.waiter import wait_until


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/{cardID}/leadGenForms
    """
)
class TestCardLeadGenFormsCustomMessageTemplate:
    @allure.title("POST leadGenForm with CustomMessageTemplateID -> PUT leadGenForm with another CustomMessageTemplateID")
    @pytest.mark.smoke
    def test_card_leadgen_form_create_and_update_with_custom_message_template(
        self,
        created_card,
        leadgen_field_template_id,
    ):
        account_id = get_card_account_id(created_card.id)

        leadgen_form_id = None
        template_id_1 = None
        template_id_2 = None
        try:
            _, template_1, _ = AccountsCustomMessageTemplatesCreateAPI().create_accounts_custom_message_template(
                account_id
            )
            template_id_1 = template_1.id
            assert template_id_1 is not None

            _, template_2, _ = AccountsCustomMessageTemplatesCreateAPI().create_accounts_custom_message_template(
                account_id
            )
            template_id_2 = template_2.id
            assert template_id_2 is not None

            leadgen_form_id = create_card_leadgen_form(
                created_card.id,
                field_template_id=leadgen_field_template_id,
                custom_message_template_id=template_id_1,
            )

            created_model = CardLeadGenFormByIdAPI().get_card_leadgen_form_by_id(created_card.id, leadgen_form_id)
            assert created_model.customMessageTemplateID == template_id_1

            updated_response, payload = CardLeadGenFormsUpdateAPI().update_card_leadgen_forms(
                created_card.id,
                leadgen_form_id=leadgen_form_id,
                field_template_id=leadgen_field_template_id,
                custom_message_template_id=template_id_2,
            )
            assert updated_response.status_code == HTTPStatus.ACCEPTED
            assert payload[0]["CustomMessageTemplateID"] == template_id_2

            updated_model = CardLeadGenFormByIdAPI().get_card_leadgen_form_by_id(created_card.id, leadgen_form_id)
            assert updated_model.customMessageTemplateID == template_id_2
        finally:
            delete_card_leadgen_form_best_effort(created_card.id, leadgen_form_id)
            if template_id_1 is not None:
                try:
                    AccountsCustomMessageTemplatesDeleteAPI().delete_accounts_custom_message_templates(
                        account_id,
                        [template_id_1],
                    )
                    deleted = wait_until(
                        lambda: _templates_absent(account_id, [int(template_id_1)]),
                        timeout_s=60,
                        step_s=3,
                    )
                    assert deleted is True, f"Custom message template id={template_id_1} still visible after delete"
                except Exception:
                    pass
            if template_id_2 is not None:
                try:
                    AccountsCustomMessageTemplatesDeleteAPI().delete_accounts_custom_message_templates(
                        account_id,
                        [template_id_2],
                    )
                    deleted = wait_until(
                        lambda: _templates_absent(account_id, [int(template_id_2)]),
                        timeout_s=60,
                        step_s=3,
                    )
                    assert deleted is True, f"Custom message template id={template_id_2} still visible after delete"
                except Exception:
                    pass


def _templates_absent(account_id: int, template_ids: list[int]) -> bool | None:
    response, model = AccountsCustomMessageTemplatesAPI().get_accounts_custom_message_templates(account_id)
    if response.status_code not in (HTTPStatus.OK, HTTPStatus.NO_CONTENT):
        return None
    present_ids = {int(item.id) for item in model.items if item.id is not None}
    return True if present_ids.isdisjoint({int(template_id) for template_id in template_ids}) else None
