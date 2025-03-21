import allure
import pytest
from config.base_test import BaseTest
from src.enums.params_enums import Params


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkWorkTypes(BaseTest):

    @pytest.mark.skip(reason='Тест на добавление типа работ есть в test_delete_marks_work_type_by_id')
    @allure.title('Test add work types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23104")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23104)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_post_add_work_type(self, param):
        self.api_work_work_types.post_add_work_type(param)

    @allure.title('Test update work type.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25190")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25190)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_put_update_work_type(self, param):
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        self.api_work_work_types.put_update_work_type(work_type_id.type[0])
        self.api_work_work_types.delete_marks_work_type_by_id(work_type_id=work_type_id.type[0])

    @allure.title('Test delete work type by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23105")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23105)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_delete_work_type_by_id(self, param):
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        self.api_work_work_types.delete_marks_work_type_by_id(work_type_id=work_type_id.type[0])

    @allure.title('Test delete work types by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25191")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25191)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_delete_work_types_by_list(self, param):
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        work_type2_id = self.api_work_work_types.post_add_work_type(param)
        work_type3_id = self.api_work_work_types.post_add_work_type(param)
        self.api_work_work_types.delete_marks_work_types_by_list(
            work_type_id.type[0],
            work_type2_id.type[0],
            work_type3_id.type[0]
        )

    @allure.title('Test get work types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23611")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23611)
    def test_get_list_work_type(self):
        self.api_work_work_types.get_list_work_type()

    @allure.title('Test returns the data for the type of work by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23118")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23118)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_get_data_work_type_by_id(self, param):
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        self.api_work_work_types.get_data_work_type_by_id(work_type_id=work_type_id.type[0])
        self.api_work_work_types.delete_marks_work_type_by_id(work_type_id=work_type_id.type[0])

    @allure.title('Test publishes work types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23119")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23119)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_put_publish_work_types(self, param):
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        self.api_work_work_types.put_publish_work_types(work_type_id=work_type_id.type[0])
        self.api_work_work_types.delete_marks_work_type_by_id(work_type_id=work_type_id.type[0])

    @allure.title('Test publishes work type by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23120")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23120)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_put_publish_work_type_by_id(self, param):
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        self.api_work_work_types.put_publish_work_type_by_id(work_type_id=work_type_id.type[0])
        self.api_work_work_types.delete_marks_work_type_by_id(work_type_id=work_type_id.type[0])

    @allure.title('Test cancels publication of work type by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23122")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23122)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_put_unpublish_work_type_by_id(self, param):
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        self.api_work_work_types.put_publish_work_type_by_id(work_type_id=work_type_id.type[0])
        self.api_work_work_types.put_unpublish_work_type_by_id(work_type_id=work_type_id.type[0])
        self.api_work_work_types.delete_marks_work_type_by_id(work_type_id=work_type_id.type[0])

    @allure.title('Test cancels publication of work types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23121")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23121)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_put_unpublish_work_types(self, param):
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        self.api_work_work_types.put_publish_work_types(work_type_id=work_type_id.type[0])
        self.api_work_work_types.put_unpublish_work_types(work_type_id=work_type_id.type[0])
        self.api_work_work_types.delete_marks_work_type_by_id(work_type_id=work_type_id.type[0])

    @allure.title('Test add check lists to work type by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25192")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25192)
    def test_post_add_check_lists_to_work_type(self):
        model_check_lists = self.api_work_checklists.post_add_checklists()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        self.api_work_work_types.post_add_check_lists_to_work_type(work_type_id, model_check_lists.result[0])
        self.api_work_checklists.delete_checklist_by_id(model_check_lists.result[0])

    @allure.title('Test get check lists from work type.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25193")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25193)
    def test_get_check_lists_from_work_type(self):
        model_check_lists = self.api_work_checklists.post_add_checklists()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        self.api_work_work_types.post_add_check_lists_to_work_type(work_type_id, model_check_lists.result[0])
        self.api_work_work_types.get_list_check_lists_work_type(work_type_id)
        self.api_work_checklists.delete_checklist_by_id(model_check_lists.result[0])

    @allure.title('Test delete check lists from work type by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25194")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25194)
    def test_delete_check_lists_from_work_type_by_list(self):
        model_check_lists = self.api_work_checklists.post_add_checklists()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        self.api_work_work_types.post_add_check_lists_to_work_type(work_type_id, model_check_lists.result[0])
        self.api_work_work_types.delete_check_lists_from_work_type(work_type_id, model_check_lists.result[0])
        self.api_work_checklists.delete_checklist_by_id(model_check_lists.result[0])

    @allure.title('Test add check list to work type by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25195")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25195)
    def test_post_add_check_list_to_work_type_by_id(self):
        model_check_lists = self.api_work_checklists.post_add_checklists()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        self.api_work_work_types.post_add_check_list_to_work_type_by_id(work_type_id, model_check_lists.result[0])
        self.api_work_checklists.delete_checklist_by_id(model_check_lists.result[0])

    @allure.title('Test delete check list from work type by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25196")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25196)
    def test_delete_check_list_from_work_type_by_id(self):
        model_check_lists = self.api_work_checklists.post_add_checklists()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        self.api_work_work_types.post_add_check_lists_to_work_type(work_type_id, model_check_lists.result[0])
        self.api_work_work_types.delete_check_list_from_work_type_by_id(work_type_id, model_check_lists.result[0])
        self.api_work_checklists.delete_checklist_by_id(model_check_lists.result[0])

    @allure.title('Test add task types to work type by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25197")
    @pytest.mark.skip(reason='Тест на добавление типа задач к виду работ проходит в - '
                             'test_delete_task_types_from_work_types_by_list')
    @pytest.mark.regress
    @pytest.mark.test_case_id(25197)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_post_add_task_types_to_work_types(self, param):
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        self.api_work_work_types.post_add_task_types_to_work_types(
            work_type_id.type[0], task_type_id[0]
        )
        self.api_work_work_types.delete_marks_work_type_by_id(work_type_id=work_type_id.type[0])

    @allure.title('Test delete task types from work type by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25198")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25198)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_delete_task_types_from_work_types_by_list(self, param):
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        self.api_work_work_types.post_add_task_types_to_work_types(
            work_type_id.type[0], task_type_id[0]
        )
        self.api_work_work_types.delete_task_types_from_work_types_by_list(
            work_type_id.type[0],
            task_type_id[0]
        )
        self.api_work_work_types.delete_marks_work_type_by_id(work_type_id=work_type_id.type[0])

    @allure.title('Test get task types from work type.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25199")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25199)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_get_task_types_from_work_types(self, param):
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        self.api_work_work_types.post_add_task_types_to_work_types(
            work_type_id.type[0], task_type_id[0]
        )
        self.api_work_work_types.get_task_types_from_work_types(work_type_id=work_type_id.type[0])
        self.api_work_work_types.delete_marks_work_type_by_id(work_type_id=work_type_id.type[0])

