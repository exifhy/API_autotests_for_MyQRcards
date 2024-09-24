from config.base_test import BaseTest
import allure
import pytest


@allure.epic("Administration")
@allure.feature("Managing common dictionaries")
class TestCommonApplications(BaseTest):

    @allure.title('Test returns a list of branches.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23389")
    @pytest.mark.regress
    def test_get_list_applications(self):
        self.api_common_applications.get_list_applications()
