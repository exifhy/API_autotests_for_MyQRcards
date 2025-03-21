import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkTaskTypes(BaseTest):

    @allure.title('Test get list task types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_task_types(self):
        self.api_work_task_types.get_list_task_types()

    @allure.title('Test update task types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_put_update_task_types(self):
        model_task_type = self.api_work_task_types.post_add_task_types()
        self.api_work_task_types.put_update_task_types(model_task_type.results[0])
        self.api_work_task_types.delete_task_types_by_id(model_task_type.results[0])

    @allure.title('Test add task type.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.skip(reason="Тест на создание типа заявки проходит в - test_delete_task_types_by_id")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_task_types(self):
        self.api_work_task_types.post_add_task_types()

    @allure.title('Test delete task type by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_task_types_by_id(self):
        model_task_type = self.api_work_task_types.post_add_task_types()
        self.api_work_task_types.delete_task_types_by_id(model_task_type.results[0])

    @allure.title('Test delete task type by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_task_types_by_list(self):
        model_task_type = self.api_work_task_types.post_add_task_types()
        model_task_type2 = self.api_work_task_types.post_add_task_types()
        model_task_type3 = self.api_work_task_types.post_add_task_types()
        self.api_work_task_types.delete_task_types_by_list(
            model_task_type.results[0],
            model_task_type2.results[0],
            model_task_type3.results[0]
        )

    @allure.title('Test get task type by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_task_types_by_id(self):
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        self.api_work_task_types.get_task_type_by_id(int(task_type_id[0]))

    @allure.title('Test route a task type by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_route_task_type(self):
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        self.api_work_task_types.get_route_task_type(int(task_type_id[0]))

    @allure.title('Test get districts task type.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_districts_task_type(self):
        model_district = self.api_es_districts.post_add_three_districts()
        model_task_type = self.api_work_task_types.post_add_task_types()
        self.api_work_task_type_district.put_update_task_type_district(
            model_task_type.results[0],
            model_district.districts[0],
            model_district.districts[1],
            model_district.districts[2]
        )
        model_list_districts = self.api_work_task_types.get_list_districts_task_type(model_task_type.results[0])
        assert str(model_district.districts[0]) in model_list_districts.root, \
            f"District ID {model_district.districts[0]} not added to task type {model_task_type.results[0]}"
        assert str(model_district.districts[1]) in model_list_districts.root, \
            f"District ID {model_district.districts[1]} not added to task type {model_task_type.results[0]}"
        assert str(model_district.districts[2]) in model_list_districts.root, \
            f"District ID {model_district.districts[2]} not added to task type {model_task_type.results[0]}"
        self.api_work_task_types.delete_task_types_by_id(model_task_type.results[0])
        self.api_es_districts.delete_districts_by_list(
            model_district.districts[0],
            model_district.districts[1],
            model_district.districts[2]
        )

    @allure.title('Test add list work types to task type.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.skip(reason="Тест на добавление вида работ к типу заявки проходит "
                             "в - test_delete_work_types_from_task_type_by_list")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_work_types_to_task_types(self):
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        model_task_type = self.api_work_task_types.post_add_task_types()
        self.api_work_task_types.post_add_work_types_to_task_types(
            model_task_type.results[0],
            work_type_id
        )
        self.api_work_task_types.delete_task_types_by_id(model_task_type.results[0])

    @allure.title('Test get list work types of task types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_work_types_task_types(self):
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        model_task_type = self.api_work_task_types.post_add_task_types()
        self.api_work_task_types.post_add_work_types_to_task_types(
            model_task_type.results[0],
            work_type_id
        )
        self.api_work_task_types.get_list_work_types_task_types(model_task_type.results[0])
        self.api_work_task_types.delete_task_types_by_id(model_task_type.results[0])

    @allure.title('Test get list work types of task types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_work_types_from_task_type_by_list(self):
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        model_task_type = self.api_work_task_types.post_add_task_types()
        self.api_work_task_types.post_add_work_types_to_task_types(
            model_task_type.results[0],
            work_type_id
        )
        self.api_work_task_types.delete_work_types_from_task_type_by_list(
            model_task_type.results[0],
            work_type_id
        )
        self.api_work_task_types.delete_task_types_by_id(model_task_type.results[0])
