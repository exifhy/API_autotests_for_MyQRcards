import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkTemplateQuickResponse(BaseTest):

    @allure.title('Test add template quick response.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.skip(reason="Тест на создание быстрого ответа проходит "
                             "в - test_delete_template_quick_response_by_list")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_template_quick_response(self):
        self.api_work_template_quick_response.post_template_quick_response()

    @allure.title('Test delete template quick response by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_template_quick_response_by_list(self):
        model_response = self.api_work_template_quick_response.post_add_two_template_quick_response()
        self.api_work_template_quick_response.delete_template_quick_response_by_list(
            model_response.results[0],
            model_response.results[1]
        )

    @allure.title('Test get list template quick response.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_template_quick_response(self):
        self.api_work_template_quick_response.get_list_template_quick_response()

    @allure.title('Test update template quick response.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_put_update_template_quick_response(self):
        model_response = self.api_work_template_quick_response.post_template_quick_response()
        self.api_work_template_quick_response.put_update_template_quick_response(model_response.results[0])
        self.api_work_template_quick_response.delete_template_quick_response_by_list(model_response.results[0])

    @allure.title('Test get template quick response by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_template_quick_response_by_id(self):
        model_response = self.api_work_template_quick_response.post_template_quick_response()
        self.api_work_template_quick_response.get_template_quick_response_by_id(model_response.results[0])
        self.api_work_template_quick_response.delete_template_quick_response_by_list(model_response.results[0])

    @allure.title('Test update bind template quick response and task types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_put_update_task_type_template_quick_response(self):
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_response = self.api_work_template_quick_response.post_template_quick_response()
        self.api_work_template_quick_response.put_update_task_type_template_quick_response(
            model_response.results[0],
            task_type_id[0]
        )
        self.api_work_template_quick_response.delete_template_quick_response_by_list(model_response.results[0])
