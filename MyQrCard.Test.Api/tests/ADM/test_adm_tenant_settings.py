import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmTenantSettings(BaseTest):

    @allure.title('Test get tenant settings.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25955")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25955)
    def test_get_tenant_settings(self):
        self.api_adm_tenant_settings.get_tenant_settings()

    @allure.title('Test get tenant settings without Authorization.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25961")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25961)
    def test_get_tenant_settings_without_authorization(self):
        self.api_adm_tenant_settings.get_tenant_settings_without_authorization()
