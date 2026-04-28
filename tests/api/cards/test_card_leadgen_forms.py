import allure
import pytest
from http import HTTPStatus

from services.cards.card_leadgen_forms.api_card_leadgen_forms import CardLeadGenFormsAPI


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/{cardID}/leadGenForms
    """
)
class TestCardLeadGenForms:
    @allure.title("POST /Cards -> GET /Cards/{id}/leadGenForms -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_card_leadgen_forms_flow(self, created_card):
        created = created_card

        response, model = CardLeadGenFormsAPI().get_card_leadgen_forms(created.id, range_header="items=0-49")
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        assert isinstance(model.items, list)
        if model.items:
            assert all(item.cardID in (None, created.id) for item in model.items)


    @allure.title("GET /Cards/{id}/leadGenForms supports offset/fetch query")
    def test_card_leadgen_forms_with_paging_query(self, created_card):
        created = created_card

        response, model = CardLeadGenFormsAPI().get_card_leadgen_forms(
            created.id,
            offset=0,
            fetch=10,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        assert isinstance(model.items, list)


    @allure.title("GET /Cards/{id}/leadGenForms without auth")
    @pytest.mark.ng
    def test_card_leadgen_forms_401_without_auth(self, created_card):
        created = created_card

        response = CardLeadGenFormsAPI().get_card_leadgen_forms_without_auth(created.id)
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)

