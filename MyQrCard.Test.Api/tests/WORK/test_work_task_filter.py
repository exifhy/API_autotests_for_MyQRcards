import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkTaskFilter(BaseTest):

    @allure.title('Test get list task filters.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24398")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24398)
    def test_get_list_task_filter(self):
        self.api_work_task_filter.get_list_task_filter()

    @allure.title('Test update task filters.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24399")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24399)
    def test_put_update_task_filters(self):
        model_filter = self.api_work_task_filter.get_list_task_filter()
        if model_filter.result[0].isAttribute is False:
            self.api_work_task_filter.put_update_task_filters(
                model_filter.result[0].id,
                attribute_id=True,
                sort=model_filter.result[0].sortOrder + 1
            )
        else:
            self.api_work_task_filter.put_update_task_filters(
                model_filter.result[0].id,
                attribute_id=False,
                sort=model_filter.result[0].sortOrder + 1
            )
