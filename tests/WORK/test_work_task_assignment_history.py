import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Actions with the tasks and attributes")
class TestWorkTaskAssignmentHistory(BaseTest):

    @allure.title('Test add  new task to a user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23315")
    @pytest.mark.smoke
    def test_post_add_new_task_to_user(self):
        model_task = self.api_work_tasks.post_add_task()
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_work_task_assignment_history.post_add_new_task_to_user(
            user_id=model_user.userID,
            task_id=model_task.id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
