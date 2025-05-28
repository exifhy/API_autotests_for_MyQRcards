import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestMsgProviders(BaseTest):

    @allure.title('Test get list providers.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25989")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25989)
    def test_get_list_providers(self):
        self.api_msg_providers.get_list_providers()
