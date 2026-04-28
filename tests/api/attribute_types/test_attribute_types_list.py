import allure
import pytest
from http import HTTPStatus

from services.attribute_types.attribute_types_list.api_attribute_types_list import (
    AttributeTypesListAPI,
)


@allure.epic("API")
@allure.feature("AttributeTypes")
@pytest.mark.api
@allure.description(
    """
    /AttributeTypes
    """
)
class TestAttributeTypesList:
    @allure.title("GET /AttributeTypes returns dictionary")
    @pytest.mark.smoke
    def test_attribute_types_list_200(self):
        response, model = AttributeTypesListAPI().get_attribute_types()

        assert response.status_code == HTTPStatus.OK, (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        assert isinstance(model.items, dict)
        assert model.items, "Attribute types payload is empty"

        first_item = next(iter(model.items.values()))
        assert first_item.code is None or first_item.code != ""
        assert first_item.name is None or first_item.name != ""
        if first_item.attributeTypeGroup is not None:
            assert first_item.attributeTypeGroup.id is not None

    @allure.title("GET /AttributeTypes without auth")
    @pytest.mark.ng
    def test_attribute_types_list_401_without_auth(self):
        response = AttributeTypesListAPI().get_attribute_types_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
