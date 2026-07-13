import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkTaskListQueries(BaseTest):

    @allure.title('Test get task list queries.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24440")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24440)
    def test_get_task_list_queries(self):
        self.api_work_task_list_queries.get_task_list_queries()

    # @allure.title('Test add task list queries.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24442")
    # @pytest.mark.regress
    # @pytest.mark.test_case_id(24442)
    # @pytest.mark.skip(reason="Тест на сохранение запроса проходит в - test_delete_task_list_queries")
    # def test_post_task_list_queries(self):
    #     model_district = self.api_es_districts.get_list_districts()
    #     work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
    #     model_query = self.api_work_task_list_queries.post_task_list_queries(
    #         model_district.result[0].id,
    #         work_type_id
    #     )
    #     self.api_work_task_list_queries.delete_task_list_queries_by_id_remove(model_query.result[0])

    @allure.title('Test update task list queries.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24443")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24443)
    def test_put_task_list_queries(self):
        model_district = self.api_es_districts.get_list_districts()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        model_query = self.api_work_task_list_queries.post_task_list_queries(
            model_district.result[0].id,
            work_type_id
        )
        self.api_work_task_list_queries.put_task_list_queries(model_query.result[0])
        self.api_work_task_list_queries.delete_task_list_queries_by_id_remove(model_query.result[0])

    @allure.title('Test delete task list queries.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24444")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24444)
    def test_delete_task_list_queries_by_list(self):
        model_district = self.api_es_districts.get_list_districts()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        model_query = self.api_work_task_list_queries.post_task_list_queries(
            model_district.result[0].id,
            work_type_id
        )
        self.api_work_task_list_queries.delete_task_list_queries_by_list(model_query.result[0])

    @allure.title('Test get task list queries by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24445")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24445)
    def test_get_task_list_queries_by_id(self):
        model_district = self.api_es_districts.get_list_districts()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        model_query = self.api_work_task_list_queries.post_task_list_queries(
            model_district.result[0].id,
            work_type_id
        )
        self.api_work_task_list_queries.get_task_list_queries_by_id(model_query.result[0])
        self.api_work_task_list_queries.delete_task_list_queries_by_id_remove(model_query.result[0])

    @allure.title('Test delete task list queries by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24446")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24446)
    def test_delete_task_list_queries_by_id(self):
        model_district = self.api_es_districts.get_list_districts()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        model_query = self.api_work_task_list_queries.post_task_list_queries(
            model_district.result[0].id,
            work_type_id
        )
        self.api_work_task_list_queries.delete_task_list_queries_by_id(model_query.result[0])

    @allure.title('Test delete task list queries by list remove.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24447")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24447)
    def test_delete_task_list_queries_by_list_remove(self):
        model_district = self.api_es_districts.get_list_districts()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        model_query = self.api_work_task_list_queries.post_task_list_queries(
            model_district.result[0].id,
            work_type_id
        )
        self.api_work_task_list_queries.delete_remove_task_list_queries_by_list(model_query.result[0])

    @allure.title('Test delete task list queries by id remove.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24448")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24448)
    def test_delete_task_list_queries_by_id_remove(self):
        model_district = self.api_es_districts.get_list_districts()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        model_query = self.api_work_task_list_queries.post_task_list_queries(
            model_district.result[0].id,
            work_type_id
        )
        self.api_work_task_list_queries.delete_task_list_queries_by_id_remove(model_query.result[0])
