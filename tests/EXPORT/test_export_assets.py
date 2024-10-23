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
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        asset_id = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        self.api_es_asset_work_types.post_add_work_type_to_asset(
            asset_id=asset_id.id,
            work_type_id=work_type_id
        )
        self.api_es_asset_districts.add_only_new_district_to_object(
            asset_id=asset_id.id,
            district_id=district_id.districts[0]
        )
        model_asset_type = self.api_es_asset_types.get_asset_type_by_id(asset_type_id)
        model_asset_class = self.api_es_asset_classes.get_asset_classes_by_id(asset_class_id)
        model_work_type = self.api_work_work_types.get_data_work_type_by_id(work_type_id)
        self.api_export_assets.get_export_list_with_set_filter_by_asset_id(
            name_asset=asset_id.name,
            asset_id=asset_id.id,
            company_name=model_company.name,
            district_name=model_district.name,
            asset_type_name=model_asset_type.name,
            asset_class_name=model_asset_class.name,
            work_type_name=model_work_type.name
        )
        self.api_es_assets.delete_object_by_id(asset_id=asset_id.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_districts.delete_district_by_id(district_id.districts[0])
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test normal export a list of objects.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23145")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23145)
    def test_get_normal_export_list_objects(self):
        self.api_export_assets.get_normal_export_list_objects()
