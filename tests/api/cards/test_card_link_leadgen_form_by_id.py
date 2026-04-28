import allure
import pytest
from http import HTTPStatus

from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.card_leadgen_forms_create.api_card_leadgen_forms_create import CardLeadGenFormsCreateAPI
from services.cards.card_leadgen_forms_delete.api_card_leadgen_forms_delete import CardLeadGenFormsDeleteAPI
from services.cards.card_link_leadgen_form_by_id.api_card_link_leadgen_form_by_id import CardLinkLeadGenFormByIdAPI
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    GET /Cards/{cardLinkId}/cardLink/leadGenForms/{formId}
    """
)
class TestCardLinkLeadGenFormById:
    @allure.title("POST leadGenForm -> GET /Cards/{cardLinkId}/cardLink/leadGenForms/{formId} -> DELETE")
    @pytest.mark.smoke
    def test_card_link_leadgen_form_by_id_200(self, created_card, leadgen_field_template_id):
        created_form = CardLeadGenFormsCreateAPI().create_card_leadgen_form(
            created_card.id,
            field_template_id=leadgen_field_template_id,
        )
        assert created_form.id is not None

        card = CardByIdAPI().get_card_by_id(created_card.id)
        assert card.url, "Card public url is empty"
        card_link_id = extract_card_link_id(card.url)

        response, model = CardLinkLeadGenFormByIdAPI().get_card_link_leadgen_form_by_id(
            card_link_id,
            created_form.id,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
        if model is not None:
            assert model.id == created_form.id

        CardLeadGenFormsDeleteAPI().delete_card_leadgen_forms(created_card.id, [created_form.id])
