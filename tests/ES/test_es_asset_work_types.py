import allure
import pytest
from config.base_test import BaseTest
from src.enums.params_enums import Params


@allure.epic("Administration")
@allure.feature("Actions with the work types")
class TestEsAssetWorkTypes(BaseTest):

    @pytest.mark.skip(reason='Work type add to asset in test - test_delete_work_type_from_asset_by_id')
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23107)
    @allure.title('Test add work type to asset.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23107")
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_post_add_work_type_to_asset(self, param):
        company_id = self.api_es_companies.post_add_our_company()
        asset_id = self.api_es_assets.post_add_object(company_id)
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        self.api_work_work_types.put_publish_complete_work_types_by_id(work_type_id=work_type_id.type[0])
        self.api_es_asset_work_types.post_add_work_type_to_asset(
            asset_id=asset_id.id,
            work_type_id=work_type_id.type[0]
        )
        self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test remove from asset work type by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23108")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23108)
    @pytest.mark.parametrize('param', Params.params_work_types.value)
    def test_delete_work_type_from_asset_by_id(self, param):
        company_id = self.api_es_companies.post_add_our_company()
        asset_id = self.api_es_assets.post_add_object(company_id)
        work_type_id = self.api_work_work_types.post_add_work_type(param)
        self.api_work_work_types.put_publish_complete_work_types_by_id(work_type_id=work_type_id.type[0])
        self.api_es_asset_work_types.post_add_work_type_to_asset(
            asset_id=asset_id.id,
            work_type_id=work_type_id.type[0]
        )
        self.api_es_asset_work_types.delete_work_type_from_asset_by_id(
            asset_id=asset_id.id,
            work_type_id=work_type_id.type[0]
        )
        self.api_work_work_types.delete_marks_work_type_by_id(work_type_id=work_type_id.type[0])
        self.api_es_companies.delete_company_by_id(company_id)

