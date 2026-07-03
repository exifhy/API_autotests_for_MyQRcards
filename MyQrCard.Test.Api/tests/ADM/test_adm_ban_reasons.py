import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmBanReasons(BaseTest):

    @allure.title('Test get list ban reasons.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25754")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25754)
    def test_get_list_ban_reasons(self):
        self.api_adm_ban_reasons.get_list_ban_reasons()
