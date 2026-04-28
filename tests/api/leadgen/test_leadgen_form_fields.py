import allure
import pytest
from http import HTTPStatus

from services.leadgen.leadgen_form_fields.api_leadgen_form_fields import (
    LeadGenFormFieldsAPI,
)


@allure.epic("API")
@allure.feature("LeadGen")
@pytest.mark.api
@allure.description(
    """
    /LeadGenFormFields
    """
)
class TestLeadGenFormFields:
    @allure.title("GET /LeadGenFormFields returns fields list")
    @pytest.mark.smoke
    def test_leadgen_form_fields_200_or_206(self):
        response, model = LeadGenFormFieldsAPI().get_leadgen_form_fields(range_header="items=0-199")

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        if response.status_code == HTTPStatus.PARTIAL_CONTENT:
            content_range = response.headers.get("Content-Range") or response.headers.get("content-range")
            assert content_range, "Expected Content-Range header for 206 response"

        assert isinstance(model.items, list)
        assert model.items, "LeadGen form fields list is empty"
        assert model.items[0].id is not None
        assert model.items[0].name is None or model.items[0].name != ""

    @allure.title("GET /LeadGenFormFields supports offset/fetch query")
    def test_leadgen_form_fields_with_paging_query(self):
        response, model = LeadGenFormFieldsAPI().get_leadgen_form_fields(offset=0, fetch=50)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        assert isinstance(model.items, list)
