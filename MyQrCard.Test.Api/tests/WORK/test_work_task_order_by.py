import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkTaskOrderBy(BaseTest):

    @allure.title('Test get task order by.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24465")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24465)
    def test_get_task_order_by(self):
        self.api_work_task_order_by.get_task_order_by()

    @allure.title('Test get task order by with range.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24466")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24466)
    def test_get_task_order_by_with_range(self):
        self.api_work_task_order_by.get_task_order_by_with_range()
