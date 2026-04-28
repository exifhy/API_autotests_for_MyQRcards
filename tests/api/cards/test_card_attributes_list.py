import allure
import pytest
from http import HTTPStatus

from services.cards.card_attributes_list.api_card_attributes_list import CardAttributesListAPI


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    GET /cards/{id}/attributes/
    """
)
class TestCardAttributesList:
    @allure.title("GET /cards/{id}/attributes/")
    @pytest.mark.smoke
    def test_card_attributes_list_200(self, created_card):
        response, model = CardAttributesListAPI().get_card_attributes(created_card.id)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
        assert isinstance(model.items, list)

    @allure.title("GET /cards/{id}/attributes/?attributeID={id} — filter by attribute")
    def test_card_attributes_list_filtered(self, created_card):
        response, model = CardAttributesListAPI().get_card_attributes(created_card.id, attribute_id=1)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
        assert isinstance(model.items, list)

    @pytest.mark.ng
    @allure.title("GET /cards/{id}/attributes/ without auth -> 401/403")
    def test_card_attributes_list_401_without_auth(self, created_card):
        response = CardAttributesListAPI().get_card_attributes_without_auth(created_card.id)
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
