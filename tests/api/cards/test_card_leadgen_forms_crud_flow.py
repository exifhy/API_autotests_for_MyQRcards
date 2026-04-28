import allure
import pytest
from http import HTTPStatus

from services.cards.card_leadgen_forms.api_card_leadgen_forms import CardLeadGenFormsAPI
from services.cards.card_leadgen_forms_update.api_card_leadgen_forms_update import (
    CardLeadGenFormsUpdateAPI,
)
from tests.api.cards.helpers import create_card_leadgen_form, delete_card_leadgen_form_best_effort


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/{cardID}/leadGenForms
    """
)
class TestCardLeadGenFormsCrudFlow:
    @allure.title("POST /Cards -> POST leadGenForm -> GET leadGenForms -> DELETE leadGenForm -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_card_leadgen_forms_crud_flow(self, created_card, leadgen_field_template_id):
        assert created_card.id is not None

        leadgen_form_id = None
        try:
            leadgen_form_id = create_card_leadgen_form(
                created_card.id,
                field_template_id=leadgen_field_template_id,
            )

            response, model = CardLeadGenFormsAPI().get_card_leadgen_forms(created_card.id)
            assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
            assert model.items, "Expected non-empty leadGenForms list after POST"
            assert any(item.id == leadgen_form_id for item in model.items if item.id is not None)
        finally:
            delete_card_leadgen_form_best_effort(created_card.id, leadgen_form_id)

    @allure.title("POST /Cards -> POST leadGenForm -> PUT leadGenForm -> GET leadGenForms -> DELETE leadGenForm -> DELETE /Cards/{id}")
    def test_card_leadgen_forms_update_flow(self, created_card, leadgen_field_template_id):
        assert created_card.id is not None

        leadgen_form_id = None
        try:
            leadgen_form_id = create_card_leadgen_form(
                created_card.id,
                field_template_id=leadgen_field_template_id,
            )

            updated_response, update_payload = CardLeadGenFormsUpdateAPI().update_card_leadgen_forms(
                created_card.id,
                leadgen_form_id=leadgen_form_id,
                field_template_id=leadgen_field_template_id,
            )
            assert updated_response.status_code == HTTPStatus.ACCEPTED

            response, model = CardLeadGenFormsAPI().get_card_leadgen_forms(created_card.id)
            assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
            target = next((item for item in model.items if item.id == leadgen_form_id), None)
            assert target is not None, "Updated leadGen form not found in GET response"
            assert target.formText == update_payload[0]["formText"]
            assert target.buttonText == update_payload[0]["buttonText"]
        finally:
            delete_card_leadgen_form_best_effort(created_card.id, leadgen_form_id)
