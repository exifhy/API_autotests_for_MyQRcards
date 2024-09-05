import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Data Export Service")
@allure.feature("Export users data")
class TestExportUsers(BaseTest):

    @allure.title('Test exports the list of users taking into account the specified filters by userID(Customers).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23172")
    @pytest.mark.smoke
    def test_get_export_list_customers_by_user_id(self):
        self.api_export_users.get_export_list_customers_by_user_id()

    @allure.title('Test exports the list of users taking into account the specified filters by userID(Employee).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23173")
    @pytest.mark.smoke
    def test_get_export_list_employee_by_user_id(self):
        self.api_export_users.get_export_list_employee_by_user_id()
