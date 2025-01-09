import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkTaskActualities(BaseTest):
    """Остальные ручки не используются"""

    @allure.title('Test get list task actualities.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24359")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24359)
    def test_get_list_task_actualities(self):
        self.api_work_task_actualities.get_list_task_actualities()
