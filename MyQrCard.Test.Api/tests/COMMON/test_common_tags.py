import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Common service offers various methods for managing common and auxiliary dictionaries.")
class TestCommonTags(BaseTest):

    @allure.title('Test get list tags.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25704")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25704)
    def test_get_list_tags(self):
        self.api_common_tags.get_list_tags()
