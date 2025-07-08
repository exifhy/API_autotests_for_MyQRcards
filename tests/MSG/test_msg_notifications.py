import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Service offers application programming interface for manipulation MSG and all connected entities..")
class TestMSGNotifications(BaseTest):

    @allure.title('Test get list of unread notifications about mass movement of 10 tasks by stages. Batch.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26618")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26618)
    def test_get_list_of_unread_notifications_about_mass_movement_tasks_by_stages(self):
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        list_tasks = self.api_work_tasks.post_create_multiple_tasks(
            task_type_id[0], 10
        )
        try:
            model_route = self.api_work_tasks.get_task_stages_next_by_list(list_tasks)
            self.api_work_task_staging_history.post_multiple_add_task_staging_history_batch(
                [model_route.results[0].nextStages[0].nextStage.id],
                [list_tasks]
            )
            self.api_msg_notifications.get_list_of_unread_notifications_about_mass_movement_tasks_by_stages(10, 15)
        finally:
            self.api_work_tasks.delete_mass_tasks_by_list(list_tasks)
