import allure
import pytest
from http import HTTPStatus

from services.attributes.attributes_list.api_attributes_list import AttributesListAPI


@allure.epic("API")
@allure.feature("Attributes")
@allure.title("GET /Attributes")
@pytest.mark.api
@pytest.mark.attributes
@allure.description(
    """
    /Attributes
    """
)
class TestAttributesList:
    @allure.title("GET /Attributes → 200, non-empty list with valid items")
    @pytest.mark.smoke
    def test_get_attributes_200(self):
        model = AttributesListAPI().get_attributes()

        assert isinstance(model.items, dict)
        assert len(model.items) > 0, "Expected non-empty attributes list"

        first_item = next(iter(model.items.values()))
        assert first_item.id >= 0
        assert first_item.name is None or first_item.name != ""

    @allure.title("GET /Attributes without auth → 401/403")
    @pytest.mark.ng
    def test_get_attributes_401_without_auth(self):
        response = AttributesListAPI().get_attributes_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
