import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkTaskStatuses(BaseTest):

    @allure.title('Test add task status.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25205")
    @pytest.mark.skip(reason='Тест на создание статуса заявки проходит в - test_delete_task_statuses_by_list')
    @pytest.mark.regress
    @pytest.mark.test_case_id(25205)
    def test_post_add_task_statuses(self):
        self.api_work_task_statuses.post_add_task_statuses()

    @allure.title('Test delete task statuses by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25206")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25206)
    def test_delete_task_statuses_by_list(self):
        task_status_id = self.api_work_task_statuses.post_add_task_statuses()
        task_status2_id = self.api_work_task_statuses.post_add_task_statuses()
        task_status3_id = self.api_work_task_statuses.post_add_task_statuses()
        self.api_work_task_statuses.delete_task_statuses_by_list(
            task_status_id.status[0],
            task_status2_id.status[0],
            task_status3_id.status[0]
        )

    @allure.title('Test update task status.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25207")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25207)
    def test_put_update_task_status(self):
        task_status_id = self.api_work_task_statuses.post_add_task_statuses()
        self.api_work_task_statuses.put_update_task_status(task_status_id.status[0])
        self.api_work_task_statuses.delete_task_statuses_by_list(task_status_id.status[0])

    @allure.title('Test get list task statuses.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25208")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25208)
    def test_get_list_task_statuses(self):
        self.api_work_task_statuses.get_list_task_statuses()

    @allure.title('Test get task status by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25209")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25209)
    def test_get_task_status_by_id(self):
        task_status_id = self.api_work_task_statuses.post_add_task_statuses()
        self.api_work_task_statuses.get_task_status_by_id(task_status_id.status[0])
        self.api_work_task_statuses.delete_task_statuses_by_list(task_status_id.status[0])

    @allure.title('Test delete task status by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25210")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25210)
    def test_delete_task_status_by_id(self):
        task_status_id = self.api_work_task_statuses.post_add_task_statuses()
        self.api_work_task_statuses.delete_task_status_by_id(task_status_id.status[0])
