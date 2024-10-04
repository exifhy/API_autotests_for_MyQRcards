import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Planning tasks")
class TestAdmUsers(BaseTest):

    @allure.title('Test add schedule for tenant.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23294")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23294)
    def test_post_add_schedule(self):
        self.api_pmp_schedules.post_add_schedule()
