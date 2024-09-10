import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Actions with the tasks and attributes")
class TestWorkTasks(BaseTest):

    @pytest.mark.skip(reason='Тест на добавление заявки есть в test_delete_marks_task_as_remote_by_id')
    @allure.title('Test add task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23230")
    @pytest.mark.smoke
    def test_add_task(self):
        self.api_work_tasks.post_add_task()

    @allure.title('Test marks the task as remote.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23231")
    @pytest.mark.smoke
    def test_delete_marks_task_as_remote_by_id(self):
        task_id = self.api_work_tasks.post_add_task()
        self.api_work_tasks.delete_task_by_id(task_id.id)
