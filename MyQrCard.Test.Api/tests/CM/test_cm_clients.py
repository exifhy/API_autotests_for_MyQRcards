from config.base_test import BaseTest
import allure
import pytest


@allure.epic("Administration")
@allure.feature("Service offers application programming interface.")
class TestCmClients(BaseTest):

    @allure.title('Test saves location data.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/29284")
    @pytest.mark.regress
    @pytest.mark.test_case_id(29284)
    def test_post_clients_locations(self):
        self.api_cm_clients.post_clients_locations()