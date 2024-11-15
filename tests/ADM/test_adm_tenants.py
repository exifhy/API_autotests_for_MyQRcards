import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmTenants(BaseTest):

    @allure.title('Test get data current tenant.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23882")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23882)
    def test_get_data_current_tenant(self):
        self.api_adm_tenants.get_data_current_tenant()
