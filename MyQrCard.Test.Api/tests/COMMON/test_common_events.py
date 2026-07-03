import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Common service offers various methods for managing common and auxiliary dictionaries.")
class TestCommonEvents(BaseTest):

    @allure.title('Test get list events.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25692")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25692)
    def test_get_list_events(self):
        self.api_common_events.get_list_events()
