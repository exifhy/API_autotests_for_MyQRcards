import allure
import pytest
from http import HTTPStatus

from services.lead_gen_form_fields.lead_gen_form_fields_list.api_lead_gen_form_fields_list import (
    LeadGenFormFieldsListAPI,
)


@allure.epic("API")
@allure.feature("LeadGenFormFields")
@pytest.mark.api
@allure.description(
    """
    GET /LeadGenFormFields
    Публичный справочник полей формы лидогенерации (FirstName, LastName, Email и т.д.).
    Авторизация не требуется.
    """
)
class TestLeadGenFormFieldsList:
    @allure.title("GET /LeadGenFormFields — returns non-empty list")
    @pytest.mark.smoke
    def test_lead_gen_form_fields_200(self):
        fields = LeadGenFormFieldsListAPI().get_lead_gen_form_fields()

        assert fields, "Expected non-empty lead gen form fields list"

    @allure.title("GET /LeadGenFormFields — each field has id, name, nameRu, nameEn")
    def test_lead_gen_form_fields_structure(self):
        fields = LeadGenFormFieldsListAPI().get_lead_gen_form_fields()

        for f in fields:
            assert f.id is not None, f"id missing: {f}"
            assert f.name, f"name is empty: {f}"
            assert f.nameRu, f"nameRu is empty: {f}"
            assert f.nameEn, f"nameEn is empty: {f}"
