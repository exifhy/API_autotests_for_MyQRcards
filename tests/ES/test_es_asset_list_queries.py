import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestEsAssetListQueries(BaseTest):

    @allure.title('Test get a list of stored queries available in the tenant.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23861")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23861)
    def test_get_list_queries_available_in_tenant(self):
        self.api_es_asset_list_queries.get_list_queries_available_in_tenant()

    @allure.title('Test add queries and binds it to the current user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23860")
    @pytest.mark.skip(reason="Тест на создание запроса проходит в - test_delete_saved_query_by_id.")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23860)
    def test_post_add_queries_binds_to_user(self, bearer_token):
        company_id = self.api_es_companies.post_add_our_company()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        district_id = self.api_es_districts.post_add_district()
        tenant_id = self.api_adm_tenants.get_data_current_tenant()
        try:
            self.api_es_asset_list_queries.post_add_queries_binds_to_user(
                token=bearer_token,
                company_id=company_id,
                work_type_id=work_type_id,
                asset_type_id=asset_type_id,
                asset_class_id=asset_class_id,
                district_id=district_id.districts[0],
                tenant_id=tenant_id.uriName
            )
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_districts.delete_district_by_id(district_id.districts[0])

    @allure.title('Test get saved query by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23869")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23869)
    def test_get_query_by_id(self, bearer_token):
        company_id = self.api_es_companies.post_add_our_company()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        district_id = self.api_es_districts.post_add_district()
        tenant_id = self.api_adm_tenants.get_data_current_tenant()
        try:
            model_query = self.api_es_asset_list_queries.post_add_queries_binds_to_user(
                token=bearer_token,
                company_id=company_id,
                work_type_id=work_type_id,
                asset_type_id=asset_type_id,
                asset_class_id=asset_class_id,
                district_id=district_id.districts[0],
                tenant_id=tenant_id.uriName
            )
            self.api_es_asset_list_queries.get_query_by_id(model_query.result[0])
            self.api_es_asset_list_queries.delete_saved_query_by_id(model_query.result[0])
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_districts.delete_district_by_id(district_id.districts[0])

    @allure.title('Test get saved query by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23869")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23869)
    def test_get_query_by_id(self, bearer_token):
        company_id = self.api_es_companies.post_add_our_company()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        district_id = self.api_es_districts.post_add_district()
        tenant_id = self.api_adm_tenants.get_data_current_tenant()
        try:
            model_query = self.api_es_asset_list_queries.post_add_queries_binds_to_user(
                token=bearer_token,
                company_id=company_id,
                work_type_id=work_type_id,
                asset_type_id=asset_type_id,
                asset_class_id=asset_class_id,
                district_id=district_id.districts[0],
                tenant_id=tenant_id.uriName
            )
            self.api_es_asset_list_queries.get_query_by_id(model_query.result[0])
            self.api_es_asset_list_queries.delete_saved_query_by_id(model_query.result[0])
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_districts.delete_district_by_id(district_id.districts[0])

    @allure.title('Test delete saved query by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23870")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23870)
    def test_delete_saved_query_by_id(self, bearer_token):
        company_id = self.api_es_companies.post_add_our_company()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        district_id = self.api_es_districts.post_add_district()
        tenant_id = self.api_adm_tenants.get_data_current_tenant()
        try:
            model_query = self.api_es_asset_list_queries.post_add_queries_binds_to_user(
                token=bearer_token,
                company_id=company_id,
                work_type_id=work_type_id,
                asset_type_id=asset_type_id,
                asset_class_id=asset_class_id,
                district_id=district_id.districts[0],
                tenant_id=tenant_id.uriName
            )
            self.api_es_asset_list_queries.delete_saved_query_by_id(model_query.result[0])
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_districts.delete_district_by_id(district_id.districts[0])

    @allure.title('Test update queries and binds it to the current user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23863")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23863)
    def test_put_update_queries(self, bearer_token):
        company_id = self.api_es_companies.post_add_our_company()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        district_id = self.api_es_districts.post_add_district()
        tenant_id = self.api_adm_tenants.get_data_current_tenant()
        try:
            model_query = self.api_es_asset_list_queries.post_add_queries_binds_to_user(
                token=bearer_token,
                company_id=company_id,
                work_type_id=work_type_id,
                asset_type_id=asset_type_id,
                asset_class_id=asset_class_id,
                district_id=district_id.districts[0],
                tenant_id=tenant_id.uriName
            )
            model_get_query = self.api_es_asset_list_queries.get_query_by_id(model_query.result[0])
            new_name_query = self.api_es_asset_list_queries.put_update_queries(
                query_id=model_query.result[0],
                tenant_id=tenant_id.uriName,
                token=bearer_token
            )
            assert model_get_query.name != new_name_query, f'{new_name_query} is equal {model_get_query.name}.'

            self.api_es_asset_list_queries.delete_saved_query_by_id(model_query.result[0])
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_districts.delete_district_by_id(district_id.districts[0])

    @allure.title('Test delete saved queries by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23867")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23867)
    def test_delete_saved_queries_by_list(self, bearer_token):
        company_id = self.api_es_companies.post_add_our_company()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        district_id = self.api_es_districts.post_add_district()
        tenant_id = self.api_adm_tenants.get_data_current_tenant()
        try:
            model_query = self.api_es_asset_list_queries.post_add_queries_binds_to_user(
                token=bearer_token,
                company_id=company_id,
                work_type_id=work_type_id,
                asset_type_id=asset_type_id,
                asset_class_id=asset_class_id,
                district_id=district_id.districts[0],
                tenant_id=tenant_id.uriName
            )
            self.api_es_asset_list_queries.delete_saved_queries_by_list(model_query.result[0])
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_districts.delete_district_by_id(district_id.districts[0])

    @allure.title('Test delete saved query by ID (remove).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23879")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23879)
    def test_delete_saved_query_by_id_remove(self, bearer_token):
        company_id = self.api_es_companies.post_add_our_company()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        district_id = self.api_es_districts.post_add_district()
        tenant_id = self.api_adm_tenants.get_data_current_tenant()
        try:
            model_query = self.api_es_asset_list_queries.post_add_queries_binds_to_user(
                token=bearer_token,
                company_id=company_id,
                work_type_id=work_type_id,
                asset_type_id=asset_type_id,
                asset_class_id=asset_class_id,
                district_id=district_id.districts[0],
                tenant_id=tenant_id.uriName
            )
            self.api_es_asset_list_queries.delete_saved_query_by_id_remove(model_query.result[0])
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_districts.delete_district_by_id(district_id.districts[0])

    @allure.title('Test delete saved queries by list (remove).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23876")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23876)
    def test_delete_saved_queries_by_list_remove(self, bearer_token):
        company_id = self.api_es_companies.post_add_our_company()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        district_id = self.api_es_districts.post_add_district()
        tenant_id = self.api_adm_tenants.get_data_current_tenant()
        try:
            model_query = self.api_es_asset_list_queries.post_add_queries_binds_to_user(
                token=bearer_token,
                company_id=company_id,
                work_type_id=work_type_id,
                asset_type_id=asset_type_id,
                asset_class_id=asset_class_id,
                district_id=district_id.districts[0],
                tenant_id=tenant_id.uriName
            )
            self.api_es_asset_list_queries.delete_saved_queries_by_list_remove(model_query.result[0])
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_districts.delete_district_by_id(district_id.districts[0])


