import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Data Export Service")
@allure.feature("Export tasks data")
class TestExportTasks(BaseTest):

    @allure.title('Test returns a list of data available for advanced exports.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23209")
    @pytest.mark.smoke
    def test_get_extended_tasks(self):
        self.api_export_tasks.get_extended_tasks()
