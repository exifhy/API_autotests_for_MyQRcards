import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmUserOrderBy(BaseTest):

    @allure.title('Test get list user order by.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26028")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(26028)
    def test_get_list_user_order_by(self):
        self.api_adm_user_order_by.get_list_user_order_by()
