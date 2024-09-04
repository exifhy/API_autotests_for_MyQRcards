import allure
import pytest
from config.base_test import BaseTest
from src.enums.params_enums import Params
import time


@allure.epic("Data Export Service")
@allure.feature("Export objects data")
class TestExportAssets(BaseTest):

    @allure.title('Test returns a list of data available for advanced exports.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23139")
    @pytest.mark.smoke
    def test_get_list_of_data_available_for_advanced_exports(self):
        self.api_export_assets.get_list_of_data_available_for_advanced_exports()

    @allure.title('Test Exports a list of objects with a set of filters (filter set in test case).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23132")
    @pytest.mark.smoke
    def test_get_export_list_with_set_filter(self):
        asset = self.api_es_assets.post_add_object()
        self.api_es_asset_districts.add_default_district_to_object(asset_id=asset.id)
        self.api_export_assets.get_export_list_with_set_filter_by_asset_id(
            name_asset=asset.name,
            asset_id=asset.id
        )

    @allure.title('Test normal export a list of objects.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23145")
    @pytest.mark.smoke
    def test_get_normal_export_list_objects(self):
        self.api_export_assets.get_normal_export_list_objects()
