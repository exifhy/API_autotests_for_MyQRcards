import allure
import pytest
from http import HTTPStatus

from services.attributes.attribute_by_id.api_attribute_by_id import AttributeByIdAPI


@allure.epic("API")
@allure.feature("Attributes")
@allure.title("GET /Attributes/{attributeID}")
@pytest.mark.api
@pytest.mark.attributes
@pytest.mark.smoke
@allure.description(
    """
    /Attributes/{attributeID}
    """
)
class TestAttributeById:
    @allure.title("GET /Attributes/{id} → 200, validate model fields")
    def test_get_attribute_by_id_200(self):
        attribute_id = 10

        model = AttributeByIdAPI().get_attribute_by_id(attribute_id)

        assert model.attribute.id == attribute_id
        assert model.type.id >= 0
        assert model.attribute.name is None or model.attribute.name != ""

    @allure.title("GET /Attributes/{id} without auth → 401/403")
    @pytest.mark.ng
    def test_get_attribute_by_id_401_without_auth(self):
        attribute_id = 10

        response = AttributeByIdAPI().get_attribute_by_id_without_auth(attribute_id)
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
