import allure
import pytest
from http import HTTPStatus

from services.cards.card_leadgen_form_by_id.api_card_leadgen_form_by_id import (
    CardLeadGenFormByIdAPI,
)
from tests.api.cards.helpers import create_card_leadgen_form, delete_card_leadgen_form_best_effort


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/{cardID}/leadGenForms/{leadGenFormID}
    """
)
class TestCardLeadGenFormById:
    @allure.title("POST /Cards -> POST leadGenForm -> GET /Cards/{cardID}/leadGenForms/{leadGenFormID} -> DELETE leadGenForm -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_card_leadgen_form_by_id_flow(self, created_card, leadgen_field_template_id):
        created_card = created_card

        leadgen_form_id = None
        try:
            leadgen_form_id = create_card_leadgen_form(
                created_card.id,
                field_template_id=leadgen_field_template_id,
            )

            model = CardLeadGenFormByIdAPI().get_card_leadgen_form_by_id(created_card.id, leadgen_form_id)
            assert model.cardID == created_card.id
            assert model.id == leadgen_form_id
            assert model.formText is not None and model.formText != ""
            assert model.buttonText is not None and model.buttonText != ""
        finally:
            delete_card_leadgen_form_best_effort(created_card.id, leadgen_form_id)


    @allure.title("GET /Cards/{cardID}/leadGenForms/{leadGenFormID} without auth")
    @pytest.mark.ng
    def test_card_leadgen_form_by_id_401_without_auth(self, created_card, leadgen_field_template_id):
        created_card = created_card

        leadgen_form_id = None
        try:
            leadgen_form_id = create_card_leadgen_form(
                created_card.id,
                field_template_id=leadgen_field_template_id,
            )

            response = CardLeadGenFormByIdAPI().get_card_leadgen_form_by_id_without_auth(
                created_card.id,
                leadgen_form_id,
            )
            assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
        finally:
            delete_card_leadgen_form_best_effort(created_card.id, leadgen_form_id)

