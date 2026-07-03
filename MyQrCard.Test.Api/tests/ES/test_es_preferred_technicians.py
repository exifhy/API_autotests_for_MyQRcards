import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestPreferredTechnicians(BaseTest):

    @pytest.mark.regress
    @pytest.mark.test_case_id(24309)
    @allure.title('Test adding a preferred technicians for an asset.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24309")
    def test_post_add_preferred_technicians(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        asset_id = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            self.api_es_preferred_technicians.post_add_preferred_technicians(
                asset_id.id,
                model_user.userID
            )
        finally:
            self.api_es_assets.delete_object_by_id(asset_id.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_es_locations.delete_location_by_id(location_id)

    @pytest.mark.regress
    @pytest.mark.test_case_id(24309)
    @allure.title('Test get preferred technicians from asset by id, user by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24309")
    def test_get_preferred_technicians_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        asset_id = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            self.api_es_preferred_technicians.post_add_preferred_technicians(
                asset_id.id,
                model_user.userID
            )
            self.api_es_preferred_technicians.get_preferred_technicians_by_id(
                asset_id.id,
                model_user.userID
            )
        finally:
            self.api_es_assets.delete_object_by_id(asset_id.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_es_locations.delete_location_by_id(location_id)

    @pytest.mark.regress
    @pytest.mark.test_case_id(24310)
    @allure.title('Test get preferred technicians.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24310")
    def test_get_preferred_technicians(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        asset_id = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            self.api_es_preferred_technicians.post_add_preferred_technicians(
                asset_id.id,
                model_user.userID
            )
            self.api_es_preferred_technicians.get_preferred_technicians()
        finally:
            self.api_es_assets.delete_object_by_id(asset_id.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_es_locations.delete_location_by_id(location_id)
