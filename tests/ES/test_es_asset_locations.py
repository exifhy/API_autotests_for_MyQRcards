import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestEsAssetLocations(BaseTest):

    @allure.title('Test add a location to an asset.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23065")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23065)
    def test_add_location_to_object(self):
        company_id = self.api_es_companies.post_add_our_company()
        created_location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            self.api_es_asset_work_types.post_add_work_type_to_asset(
                asset_id=object_model.id,
                work_type_id=work_type_id
            )
            self.api_es_assetlocations.add_location_to_object(
                asset_id=object_model.id,
                location_id=created_location_id
            )
        finally:
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test deleting location binding to an asset.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23066")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23066)
    def test_delete_location_from_object(self):
        company_id = self.api_es_companies.post_add_our_company()
        created_location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            self.api_es_asset_work_types.post_add_work_type_to_asset(
                asset_id=object_model.id,
                work_type_id=work_type_id
            )
            self.api_es_assetlocations.add_location_to_object(
                asset_id=object_model.id,
                location_id=created_location_id
            )
            self.api_es_assetlocations.delete_location_from_object(
                asset_id=object_model.id
            )
        finally:
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list of locations by asset.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23815")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23815)
    def test_get_location_by_object(self):
        company_id = self.api_es_companies.post_add_our_company()
        created_location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            self.api_es_asset_work_types.post_add_work_type_to_asset(
                asset_id=object_model.id,
                work_type_id=work_type_id
            )
            self.api_es_assetlocations.add_location_to_object(
                asset_id=object_model.id,
                location_id=created_location_id
            )
            self.api_es_assetlocations.get_location_by_object(
                asset_id=object_model.id
            )
        finally:
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test updating the time an asset is on location.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23814")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23814)
    def test_put_update_time_an_asset_on_location(self):
        company_id = self.api_es_companies.post_add_our_company()
        created_location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            self.api_es_asset_work_types.post_add_work_type_to_asset(
                asset_id=object_model.id,
                work_type_id=work_type_id
            )
            self.api_es_assetlocations.add_location_to_object(
                asset_id=object_model.id,
                location_id=created_location_id
            )
            self.api_es_assetlocations.put_update_time_an_asset_on_location(
                asset_id=object_model.id,
                location_id=created_location_id
            )
        finally:
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(created_location_id)
