import allure
import pytest
from config.base_test import BaseTest
from src.enums.params_enums import Params
import time


@allure.epic("Administration")
@allure.feature("Actions with the tasks and attributes")
class TestWorkWorkTypes(BaseTest):

    @pytest.mark.skip(reason='Тест на добавление типа работ есть в test_delete_marks_work_type_by_id')
    @allure.title('Test add work types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23104")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23104)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_post_add_work_type(self, param):
        self.api_work_work_types.post_add_work_type(param)

    @allure.title('Test delete work types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23105")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23105)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_delete_marks_work_type_by_id(self, param):
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        self.api_work_work_types.delete_marks_work_type_by_id(work_type_id=work_type_id.type[0])

    @allure.title('Test returns the data for the type of work by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23118")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23118)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_get_data_work_type_by_id(self, param):
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        self.api_work_work_types.get_data_work_type_by_id(work_type_id=work_type_id.type[0])
        self.api_work_work_types.delete_marks_work_type_by_id(work_type_id=work_type_id.type[0])

    @allure.title('Test publishes completed works.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23119")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23119)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_put_publish_complete_work_types(self, param):
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        self.api_work_work_types.put_publish_complete_work_types(work_type_id=work_type_id.type[0])
        self.api_work_work_types.delete_marks_work_type_by_id(work_type_id=work_type_id.type[0])

    @allure.title('Test publishes completed works.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23120")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23120)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_put_publish_complete_work_types_by_id(self, param):
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        self.api_work_work_types.put_publish_complete_work_types_by_id(work_type_id=work_type_id.type[0])
        self.api_work_work_types.delete_marks_work_type_by_id(work_type_id=work_type_id.type[0])

    @allure.title('Test cancels publication of completed work by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23122")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23122)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_put_unpublish_complete_work_types_by_id(self, param):
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        self.api_work_work_types.put_publish_complete_work_types_by_id(work_type_id=work_type_id.type[0])
        self.api_work_work_types.put_unpublish_complete_work_types_by_id(work_type_id=work_type_id.type[0])
        self.api_work_work_types.delete_marks_work_type_by_id(work_type_id=work_type_id.type[0])

    @allure.title('Test cancels publication of completed work.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23121")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23121)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_put_unpublish_complete_work_types(self, param):
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        self.api_work_work_types.put_publish_complete_work_types(work_type_id=work_type_id.type[0])
        self.api_work_work_types.put_unpublish_complete_work_types(work_type_id=work_type_id.type[0])
        self.api_work_work_types.delete_marks_work_type_by_id(work_type_id=work_type_id.type[0])
