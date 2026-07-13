import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmUserTaskListQueries(BaseTest):

    @allure.title('Test add user task list queries.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26177")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26177)
    def test_post_add_user_task_list_queries(self, bearer_token):
        model_user_stuff = self.api_adm_users.post_add_user_staff()
        model_district = self.api_es_districts.get_list_districts()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        model_query = self.api_work_task_list_queries.post_task_list_queries_by_owner_user(
            model_district.result[0].id,
            work_type_id,
            bearer_token
        )
        self.api_adm_user_task_list_queries.post_add_user_task_list_queries(
            model_user_stuff.userID,
            model_query.result[0]
        )
        model_query_stuff = self.api_adm_users.get_list_task_queries_to_user_by_id(model_user_stuff.userID)
        assert int(model_query.result[0]) == int(next(iter(model_query_stuff.root))), \
            f"Task list queries ID {model_query.result[0]} has not been added to the user iD {model_user_stuff.userID}"
        self.api_adm_users.delete_user_by_id(model_user_stuff.userID)
        self.api_work_task_list_queries.delete_task_list_queries_by_list_by_owner_user(
            bearer_token,
            model_query.result[0]
        )

    @allure.title('Test delete user task list queries.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26178")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26178)
    def test_delete_user_task_list_queries(self):
        model_api_user = self.api_adm_tenant_members.get_api_user_in_current_tenant()
        model_district = self.api_es_districts.get_list_districts()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        model_query = self.api_work_task_list_queries.post_task_list_queries(
            model_district.result[0].id,
            work_type_id
        )
        self.api_adm_user_task_list_queries.delete_user_task_list_queries(
            model_api_user.user.id,
            model_query.result[0]
        )
        self.api_work_task_list_queries.delete_task_list_queries_by_id(model_query.result[0])
