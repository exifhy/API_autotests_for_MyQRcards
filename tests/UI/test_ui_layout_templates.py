import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("UI service for providing components and controls info for front-end application part.")
class TestUILayoutTemplates(BaseTest):

    @allure.title('Test get list task layout templates.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26977")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26977)
    def test_get_list_task_layout_templates(self):
        self.api_ui_layout_templates.get_list_task_layout_templates()
