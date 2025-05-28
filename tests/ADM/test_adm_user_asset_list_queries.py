import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmUserAssetListQueries(BaseTest):

    @allure.title('Test add user asset list queries by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25968")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25968)
    def test_post_add_user_asset_list_queries_by_list(self, bearer_token):
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        tenant_id = self.api_adm_tenants.get_data_current_tenant()
        model_user = self.api_adm_users.post_add_user_customer()
        model_queries = self.api_es_asset_list_queries.post_add_asset_list_queries_only_asset_type(
            bearer_token, asset_type_id, tenant_id.uriName
        )
        try:
            self.api_adm_user_asset_list_queries.post_add_user_asset_list_queries_by_list(
                model_user.userID, model_queries.result[0]
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_es_asset_list_queries.delete_saved_query_by_id_remove(model_queries.result[0])

    @allure.title('Test add user asset list queries.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_user_asset_list_queries(self, bearer_token):
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        tenant_id = self.api_adm_tenants.get_data_current_tenant()
        model_user = self.api_adm_users.post_add_user_customer()
        model_queries = self.api_es_asset_list_queries.post_add_asset_list_queries_only_asset_type(
            bearer_token, asset_type_id, tenant_id.uriName
        )
        try:
            self.api_adm_user_asset_list_queries.post_add_user_asset_list_queries(
                model_user.userID, model_queries.result[0]
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_es_asset_list_queries.delete_saved_query_by_id_remove(model_queries.result[0])

    @allure.title('Test delete user asset list queries.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_user_asset_list_queries(self, bearer_token):
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        tenant_id = self.api_adm_tenants.get_data_current_tenant()
        model_user = self.api_adm_users.post_add_user_customer()
        model_queries = self.api_es_asset_list_queries.post_add_asset_list_queries_only_asset_type(
            bearer_token, asset_type_id, tenant_id.uriName
        )
        try:
            self.api_adm_user_asset_list_queries.post_add_user_asset_list_queries(
                model_user.userID, model_queries.result[0]
            )
            self.api_adm_user_asset_list_queries.delete_user_asset_list_queries(
                model_user.userID, model_queries.result[0]
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_es_asset_list_queries.delete_saved_query_by_id_remove(model_queries.result[0])

    @allure.title('Test delete user asset list queries by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_user_asset_list_queries_by_list(self, bearer_token):
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        tenant_id = self.api_adm_tenants.get_data_current_tenant()
        model_user = self.api_adm_users.post_add_user_customer()
        model_queries = self.api_es_asset_list_queries.post_add_asset_list_queries_only_asset_type(
            bearer_token, asset_type_id, tenant_id.uriName
        )
        try:
            self.api_adm_user_asset_list_queries.post_add_user_asset_list_queries_by_list(
                model_user.userID, model_queries.result[0]
            )
            self.api_adm_user_asset_list_queries.delete_user_asset_list_queries_by_list(
                model_user.userID, model_queries.result[0]
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_es_asset_list_queries.delete_saved_query_by_id_remove(model_queries.result[0])
