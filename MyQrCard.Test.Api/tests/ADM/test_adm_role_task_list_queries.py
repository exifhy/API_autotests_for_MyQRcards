import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmRoleTaskListQueriesAPI(BaseTest):

    @allure.title('Test add stored task list queries for a role.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30346")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30346)
    def test_post_role_task_list_queries(self):
        model_query = None
        role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
        model_district = self.api_es_districts.get_list_districts()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        try:
            model_query = self.api_work_task_list_queries.post_task_list_queries(
                model_district.result[0].id,
                work_type_id
            )
            self.api_adm_role_task_list_queries.post_role_task_list_queries(
                role_id,
                model_query.result[0]
            )
        finally:
            self.api_work_task_list_queries.delete_task_list_queries_by_list(model_query.result[0])

    @allure.title('Test delete stored task list queries for a role.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30347")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30347)
    def test_delete_role_task_list_queries(self):
        model_query = None
        role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
        model_district = self.api_es_districts.get_list_districts()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        try:
            model_query = self.api_work_task_list_queries.post_task_list_queries(
                model_district.result[0].id,
                work_type_id
            )
            model_role_task_list_queries = self.api_adm_role_task_list_queries.post_role_task_list_queries(
                role_id,
                model_query.result[0]
            )
            self.api_adm_role_task_list_queries.delete_role_task_list_queries(
                role_id,
                model_role_task_list_queries.results[0].taskListQueryID
            )
        finally:
            self.api_work_task_list_queries.delete_task_list_queries_by_list(model_query.result[0])

    @allure.title('Test verify post role task list queries invalid payload.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30348")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30348)
    def test_post_role_task_list_queries_invalid_payload(self):
        self.api_adm_role_task_list_queries.post_role_task_list_queries_invalid_payload()

    @allure.title('Test verify post role task list queries without auth.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30349")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30349)
    def test_post_role_task_list_queries_without_auth(self):
        self.api_adm_role_task_list_queries.post_role_task_list_queries_without_auth()

    @allure.title('Test verify post role task list queries with invalid app id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30350")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30350)
    def test_post_role_task_list_queries_invalid_app_id(self):
        self.api_adm_role_task_list_queries.post_role_task_list_queries_invalid_app_id()

    @allure.title('Test verify delete role task list queries invalid payload ([]).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30351")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30351)
    def test_delete_role_task_list_queries_invalid_payload(self):
        self.api_adm_role_task_list_queries.delete_role_task_list_queries_invalid_payload()

    @allure.title('Test verify delete role task list queries without auth.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30352")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30352)
    def test_delete_role_task_list_queries_without_auth(self):
        self.api_adm_role_task_list_queries.delete_role_task_list_queries_without_auth()

    @allure.title('Test verify delete role task list queries with invalid app id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30345")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30345)
    def test_delete_role_task_list_queries_invalid_app_id(self):
        self.api_adm_role_task_list_queries.delete_role_task_list_queries_invalid_app_id()