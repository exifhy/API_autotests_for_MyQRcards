import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Data Export Service")
@allure.feature("Export objects data")
class TestExportAssets(BaseTest):

    @allure.title('Test returns a list of data available for extended exports.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23139")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23139)
    def test_get_list_of_data_available_for_extended_exports(self):
        self.api_export_assets.get_list_of_data_available_for_extended_exports()

    @allure.title('Test Exports a list of objects with a set of filters (filter set in test case).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23132")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23132)
    def test_get_export_list_with_set_filter(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        district_id = self.api_es_districts.post_add_district()
        model_company = self.api_es_companies.get_detailed_information_on_company_by_id(company_id)
        model_district = self.api_es_districts.get_detail_district_info_by_id(district_id.districts[0])
        asset = self.api_es_assets.post_add_object(company_id)
        self.api_es_asset_districts.add_only_new_district_to_object(
            asset_id=asset.id,
            district_id=district_id.districts[0]
        )
        self.api_export_assets.get_export_list_with_set_filter_by_asset_id(
            name_asset=asset.name,
            asset_id=asset.id,
            company_name=model_company.name,
            district_name=model_district.name
        )
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_districts.delete_district_by_id(district_id.districts[0])

    @allure.title('Test normal export a list of objects.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23145")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23145)
    def test_get_normal_export_list_objects(self):
        self.api_export_assets.get_normal_export_list_objects()
