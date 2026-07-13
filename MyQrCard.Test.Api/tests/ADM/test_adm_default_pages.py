import allure
import pytest
from config.base_test import BaseTest
from src.enums.params_enums import Params


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmDefaultPages(BaseTest):

    @allure.title('Test get list default pages.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30281")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30281)
    def test_get_list_default_pages(self):
        self.api_adm_default_pages.get_list_default_pages()

    @allure.title('Test get list default pages without token.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30282")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30282)
    def test_get_list_default_pages_without_token(self):
        self.api_adm_default_pages.get_list_default_pages_without_token()

    @allure.title('Test get list default pages with invalid token.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30283")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30283)
    def test_get_list_default_pages_invalid_token(self):
        self.api_adm_default_pages.get_list_default_pages_invalid_token()

    @allure.title('Test get list default pages with invalid app id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30284")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30284)
    def test_get_list_default_pages_invalid_app_id(self):
        self.api_adm_default_pages.get_list_default_pages_invalid_app_id()

    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30285")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30285)
    @pytest.mark.parametrize('content_type', Params.params_content_type_body.value)
    def test_get_list_default_pages_content_type_text_plain(self, content_type, request):
        allure.dynamic.title(f"{request.node.callspec.id}")
        self.api_adm_default_pages.get_list_default_pages_with_content_type(content_type)

    @allure.title('Test get list default pages measure response time.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30286")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30286)
    def test_get_list_default_pages_measure_time(self):
        self.api_adm_default_pages.get_list_default_pages_measure_time()

    @allure.title('Test get list default pages idempotency.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30287")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30287)
    def test_get_list_default_pages_idempotent(self):
        self.api_adm_default_pages.get_list_default_pages_idempotent()

    @allure.title('Test get list default pages concurrent requests.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30288")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30288)
    def test_get_list_default_pages_concurrent(self):
        self.api_adm_default_pages.get_list_default_pages_concurrent()

    @allure.title('Test get list default pages verify forbidden access.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30289")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30289)
    def test_get_list_default_pages_forbidden(self):
        self.api_adm_default_pages.get_list_default_pages_forbidden()
