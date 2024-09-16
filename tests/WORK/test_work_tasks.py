import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Actions with the tasks and attributes")
class TestWorkTasks(BaseTest):

    @pytest.mark.skip(reason='Тест на добавление заявки есть в test_delete_marks_task_as_remove_by_id')
    @allure.title('Test add task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23230")
    @pytest.mark.smoke
    def test_add_task(self):
        self.api_work_tasks.post_add_task()

    @allure.title('Test marks the task as remove.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23231")
    @pytest.mark.smoke
    def test_delete_marks_task_as_remove_by_id(self):
        task_id = self.api_work_tasks.post_add_task()
        self.api_work_tasks.delete_task_by_id(task_id.id)

    @allure.title('Test returns a list of tasks available to the user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23258")
    @pytest.mark.smoke
    def test_get_list_of_tasks_available_to_user(self):
        self.api_work_tasks.get_list_of_tasks_available_to_user()

    @allure.title('Test returns detailed information on the task by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23264")
    @pytest.mark.smoke
    def test_get_detailed_info_task_by_id(self):
        model_task = self.api_work_tasks.post_add_task()
        self.api_work_tasks.get_detailed_info_task_by_id(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)

    @allure.title('Test update task by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23265")
    @pytest.mark.smoke
    def test_put_update_task_by_id(self):
        model_task = self.api_work_tasks.post_add_task()
        task_number, note_task = self.api_work_tasks.put_update_task_by_id(model_task.id)
        model_info_task = self.api_work_tasks.get_detailed_info_task_by_id(model_task.id)
        assert model_info_task.number == task_number, f'Expected {model_info_task.number}, but got {task_number}'
        assert model_info_task.notes == note_task, f'Expected {model_info_task.notes}, but got {note_task}'
        self.api_work_tasks.delete_task_by_id(model_task.id)
