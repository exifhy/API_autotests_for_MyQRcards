import allure
import pytest
from config.base_test import BaseTest
from src.enums.params_enums import Params


@allure.epic("Administration")
@allure.feature("Actions with the tasks and attributes")
class TestWorkTaskStagingHistory(BaseTest):

    @allure.title('Test actual record to the history of the task progress by stage.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23331")
    @pytest.mark.smoke
    @pytest.mark.parametrize('task_stage_id', Params.params_task_staging_status.value)
    def test_post_add_task_staging_history(self, task_stage_id):
        model_task = self.api_work_tasks.post_add_task()
        self.api_work_task_staging_history.post_add_task_staging_history(
            stage_id=task_stage_id,
            task_id=model_task.id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)


