import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_card_leadgen_form_by_id.api_accounts_card_leadgen_form_by_id import (
    AccountsCardLeadGenFormByIdAPI,
)
from services.accounts.accounts_card_leadgen_forms.api_accounts_card_leadgen_forms import (
    AccountsCardLeadGenFormsAPI,
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
from services.cards.card_by_id.api_card_by_id import CardByIdAPI


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    /Accounts/{accountID}/Cards/{cardID}/leadGenForms
    """
)
class TestAccountsCardLeadGenForms:
    @allure.title("POST /Cards -> POST /Accounts/{accountID}/Cards/{cardID}/leadGenForms -> GET list -> GET by id")
    @pytest.mark.smoke
    def test_accounts_card_leadgen_forms_crud_flow(self, created_card, leadgen_field_template_id):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        created_form = AccountsCardLeadGenFormsCreateAPI().create_accounts_card_leadgen_form(
            card.accountID,
            created.id,
            field_template_id=leadgen_field_template_id,
        )
        assert created_form.id is not None

        response, model = AccountsCardLeadGenFormsAPI().get_accounts_card_leadgen_forms(card.accountID, created.id)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        assert any(item.id == created_form.id for item in model.items if item.id is not None)

        by_id_model = AccountsCardLeadGenFormByIdAPI().get_accounts_card_leadgen_form_by_id(
            card.accountID,
            created.id,
            created_form.id,
        )
        assert by_id_model.id == created_form.id
        assert by_id_model.cardID == created.id

        updated_response, payload = AccountsCardLeadGenFormsUpdateAPI().update_accounts_card_leadgen_forms(
            card.accountID,
            created.id,
            leadgen_form_id=created_form.id,
            field_template_id=leadgen_field_template_id,
        )
        assert updated_response.status_code == HTTPStatus.ACCEPTED

        refreshed = AccountsCardLeadGenFormByIdAPI().get_accounts_card_leadgen_form_by_id(
            card.accountID,
            created.id,
            created_form.id,
        )
        assert refreshed.formText == payload[0]["formText"]
        assert refreshed.buttonText == payload[0]["buttonText"]

        deleted = AccountsCardLeadGenFormsDeleteAPI().delete_accounts_card_leadgen_forms(
            card.accountID,
            created.id,
            [created_form.id],
        )
        assert deleted.status_code == HTTPStatus.ACCEPTED

        response_after_delete, model_after_delete = AccountsCardLeadGenFormsAPI().get_accounts_card_leadgen_forms(
            card.accountID,
            created.id,
        )
        assert response_after_delete.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        assert all(item.id != created_form.id for item in model_after_delete.items if item.id is not None)

    @allure.title("GET /Accounts/{accountID}/Cards/{cardID}/leadGenForms supports offset/fetch query")
    def test_accounts_card_leadgen_forms_with_paging_query(self, created_card):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        response, model = AccountsCardLeadGenFormsAPI().get_accounts_card_leadgen_forms(
            card.accountID,
            created.id,
            offset=0,
            fetch=10,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        assert isinstance(model.items, list)

    @allure.title("GET /Accounts/{accountID}/Cards/{cardID}/leadGenForms without auth")
    @pytest.mark.ng
    def test_accounts_card_leadgen_forms_without_auth(self, created_card):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        response = AccountsCardLeadGenFormsAPI().get_accounts_card_leadgen_forms_without_auth(
            card.accountID,
            created.id,
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
