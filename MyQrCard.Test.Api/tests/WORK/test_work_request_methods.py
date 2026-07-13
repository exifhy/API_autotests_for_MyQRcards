import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkRequestMethods(BaseTest):

    @allure.title('Test get list request methods orders task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24341")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24341)
    def test_get_request_methods(self):
        self.api_work_request_methods.get_request_methods()
