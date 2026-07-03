import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Common service offers various methods for managing common and auxiliary dictionaries.")
class TestCommonSystemTags(BaseTest):

    @allure.title('Test get list system tags.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25702")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25702)
    def test_get_list_system_tags(self):
        self.api_common_system_tags.get_list_system_tags()
