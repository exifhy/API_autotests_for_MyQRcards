import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("UI service for providing components and controls info for front-end application part.")
class TestUIComponents(BaseTest):

    @allure.title('Test get list components.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27028")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27028)
    def test_get_list_components(self):
        self.api_ui_components.get_list_components()
