import allure
import pytest
from http import HTTPStatus

from services.attribute_forms.attribute_forms_list.api_attribute_forms_list import (
    AttributeFormsListAPI,
)


@allure.epic("API")
@allure.feature("AttributeForms")
@pytest.mark.api
@allure.description(
    """
    /AttributeForms
    """
)
class TestAttributeFormsList:
    @allure.title("GET /AttributeForms returns forms list")
    @pytest.mark.smoke
    def test_attribute_forms_list_200_or_206(self):
        response, model = AttributeFormsListAPI().get_attribute_forms(range_header="items=0-199")

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        if response.status_code == HTTPStatus.PARTIAL_CONTENT:
            content_range = response.headers.get("Content-Range") or response.headers.get("content-range")
            assert content_range, "Expected Content-Range header for 206 response"

        assert isinstance(model.items, list)
        assert model.items, "Attribute forms list is empty"
        assert model.items[0].id is not None
        assert model.items[0].name is None or model.items[0].name != ""

    @allure.title("GET /AttributeForms supports offset/fetch query")
    def test_attribute_forms_list_with_paging_query(self):
        response, model = AttributeFormsListAPI().get_attribute_forms(offset=0, fetch=50)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        assert isinstance(model.items, list)

    @allure.title("GET /AttributeForms without auth")
    @pytest.mark.ng
    def test_attribute_forms_list_401_without_auth(self):
        response = AttributeFormsListAPI().get_attribute_forms_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
