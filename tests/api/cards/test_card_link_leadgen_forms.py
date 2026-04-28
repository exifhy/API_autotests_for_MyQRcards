import allure
import pytest
from http import HTTPStatus

from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.card_leadgen_forms_create.api_card_leadgen_forms_create import (
    CardLeadGenFormsCreateAPI,
)
from services.cards.card_leadgen_forms_delete.api_card_leadgen_forms_delete import (
    CardLeadGenFormsDeleteAPI,
)
from services.cards.card_link_leadgen_forms.api_card_link_leadgen_forms import (
    CardLinkLeadGenFormsAPI,
)
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/{id}/cardLink/leadGenForms
    """
)
class TestCardLinkLeadGenForms:
    @allure.title("POST /Cards -> POST leadGenForm -> GET /Cards/{cardLinkId}/cardLink/leadGenForms -> DELETE leadGenForm -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_card_link_leadgen_forms_flow(self, created_card, leadgen_field_template_id):
        created_card = created_card

        created_form = CardLeadGenFormsCreateAPI().create_card_leadgen_form(
            created_card.id,
            field_template_id=leadgen_field_template_id,
        )
        assert created_form.id is not None

        card = CardByIdAPI().get_card_by_id(created_card.id)
        assert card.url, "Card public url is empty"
        card_link_id = extract_card_link_id(card.url)

        response, model = CardLinkLeadGenFormsAPI().get_card_link_leadgen_forms(
            card_link_id,
            range_header="items=0-49",
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        assert model.items, "Expected non-empty leadGen forms list for card link"
        assert any(item.id == created_form.id for item in model.items if item.id is not None)

        deleted_form = CardLeadGenFormsDeleteAPI().delete_card_leadgen_forms(
            created_card.id,
            [created_form.id],
        )
        assert deleted_form.status_code == HTTPStatus.ACCEPTED


    @allure.title("GET /Cards/{cardLinkId}/cardLink/leadGenForms supports offset/fetch query")
    def test_card_link_leadgen_forms_with_paging_query(self, created_card, leadgen_field_template_id):
        created_card = created_card

        created_form = CardLeadGenFormsCreateAPI().create_card_leadgen_form(
            created_card.id,
            field_template_id=leadgen_field_template_id,
        )
        assert created_form.id is not None

        card = CardByIdAPI().get_card_by_id(created_card.id)
        assert card.url, "Card public url is empty"
        card_link_id = extract_card_link_id(card.url)

        response, model = CardLinkLeadGenFormsAPI().get_card_link_leadgen_forms(
            card_link_id,
            offset=0,
            fetch=10,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        assert model.items, "Expected non-empty leadGen forms list for card link"

        deleted_form = CardLeadGenFormsDeleteAPI().delete_card_leadgen_forms(
            created_card.id,
            [created_form.id],
        )
        assert deleted_form.status_code == HTTPStatus.ACCEPTED

