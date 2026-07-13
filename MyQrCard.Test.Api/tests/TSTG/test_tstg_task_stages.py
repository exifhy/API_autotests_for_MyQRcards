import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Service offers application programming interface for manipulation with task stages and task life cycle."
)
class TestTstgTaskStages(BaseTest):

    @allure.title('Test get list task stages in tenant.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23784")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23784)
    def test_get_list_task_stages_in_tenant(self):
        self.api_tstg_task_stages.get_list_task_stages_in_tenant()
