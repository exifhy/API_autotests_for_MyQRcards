import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_custom_message_templates.api_accounts_custom_message_templates import (
    AccountsCustomMessageTemplatesAPI,
)
from services.accounts.accounts_custom_message_templates_create.api_accounts_custom_message_templates_create import (
    AccountsCustomMessageTemplatesCreateAPI,
)
from services.accounts.accounts_custom_message_templates_delete.api_accounts_custom_message_templates_delete import (
    AccountsCustomMessageTemplatesDeleteAPI,
)
from services.accounts.accounts_custom_message_template_by_id.api_accounts_custom_message_template_by_id import (
    AccountsCustomMessageTemplateByIdAPI,
)
from services.accounts.accounts_custom_message_templates_update.api_accounts_custom_message_templates_update import (
    AccountsCustomMessageTemplatesUpdateAPI,
)
from services.cards.card_by_id.api_card_by_id import CardByIdAPI


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    /Accounts/{accountID}/CustomMessageTemplates
    """
)
class TestAccountsCustomMessageTemplates:
    @allure.title("POST /Cards -> POST template -> GET list -> GET by id -> PUT -> DELETE template")
    @pytest.mark.smoke
    def test_accounts_custom_message_templates_crud_flow(self, created_card):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        create_response, created_template, create_payload = (
            AccountsCustomMessageTemplatesCreateAPI().create_accounts_custom_message_template(card.accountID)
        )
        assert create_response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED)
        assert created_template.id is not None, "Custom message template id is empty"

        list_response, list_model = AccountsCustomMessageTemplatesAPI().get_accounts_custom_message_templates(
            card.accountID
        )
        assert list_response.status_code == HTTPStatus.OK
        assert any(item.id == created_template.id for item in list_model.items if item.id is not None)

        by_id_model = AccountsCustomMessageTemplateByIdAPI().get_accounts_custom_message_template_by_id(
            card.accountID,
            created_template.id,
        )
        assert by_id_model.id == created_template.id
        assert by_id_model.subjectTemplate == create_payload["subjectTemplate"]

        update_response, update_payload = AccountsCustomMessageTemplatesUpdateAPI().update_accounts_custom_message_template(
            card.accountID,
            created_template.id,
        )
        assert update_response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT)

        updated_model = AccountsCustomMessageTemplateByIdAPI().get_accounts_custom_message_template_by_id(
            card.accountID,
            created_template.id,
        )
        assert updated_model.subjectTemplate == update_payload["subjectTemplate"]
        assert updated_model.contentTemplate == update_payload["contentTemplate"]

        delete_response = AccountsCustomMessageTemplatesDeleteAPI().delete_accounts_custom_message_templates(
            card.accountID,
            [created_template.id],
        )
        assert delete_response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT)

        final_response, final_model = AccountsCustomMessageTemplatesAPI().get_accounts_custom_message_templates(
            card.accountID
        )
        assert final_response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
        assert all(item.id != created_template.id for item in final_model.items if item.id is not None)

