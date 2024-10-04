import allure
from config.base_test import BaseTest
import pytest


@allure.epic("Administration")
@allure.feature("Actions with the districts")
class TestEsAssetDistricts(BaseTest):

    @allure.title('Test Adds a districts to an object.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23096")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23096)
    def test_add_district_to_object(self):
        district_id = self.api_es_districts.post_add_district()
        company_id = self.api_es_companies.post_add_our_company()
        asset_id = self.api_es_assets.post_add_object(company_id)
        self.api_es_asset_districts.add_district_to_object(asset_id=asset_id.id, district_id=district_id.districts[0])
        self.api_es_districts.delete_district_by_id(district_id=district_id.districts[0])
        self.api_es_assets.delete_object_by_id(asset_id=asset_id.id)
        self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test remove a districts from the object.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23097")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23097)
    def test_remove_district_from_object(self):
        district_id = self.api_es_districts.post_add_district()
        company_id = self.api_es_companies.post_add_our_company()
        asset_id = self.api_es_assets.post_add_object(company_id)
        self.api_es_asset_districts.add_district_to_object(asset_id=asset_id.id, district_id=district_id.districts[0])
        self.api_es_asset_districts.delete_district_from_object(asset_id.id, district_id.districts[0])
        self.api_es_assets.delete_object_by_id(asset_id=asset_id.id)
        self.api_es_companies.delete_company_by_id(company_id)
