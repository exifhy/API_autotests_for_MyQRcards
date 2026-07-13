import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Service offers application programming interface for manipulation personnel and all connected entities."
)
class TestPaAssetAssignments(BaseTest):

    @allure.title('Test get list asset assignments by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26054")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26054)
    def test_get_list_asset_assignments_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        self.api_pa_asset_assignments.post_add_asset_assignments(
            model_user.userID,
            object_model.id
        )
        self.api_pa_asset_assignments.get_list_asset_assignments_by_user_id(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    # @allure.title('Test add asset assignments by user ID.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26055")
    # @pytest.mark.regress
    # @pytest.mark.test_case_id(26055)
    # @pytest.mark.skip(
    #     reason="Тест на добавление объекта для пользователя проходит в - test_get_list_asset_assignments_by_user_id"
    # )
    # def test_post_add_asset_assignments(self):
    #     model_user = self.api_adm_users.post_add_user_staff()
    #     company_id = self.api_es_companies.post_add_our_company()
    #     location_id = self.api_es_locations.post_add_location()
    #     self.api_es_company_locations.post_add_company_locations(
    #         company_id=company_id,
    #         location_id=location_id
    #     )
    #     asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
    #     asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
    #     object_model = self.api_es_assets.post_add_object(
    #         company_id=company_id,
    #         asset_class_id=asset_class_id,
    #         asset_type_id=asset_type_id
    #     )
    #     self.api_pa_asset_assignments.post_add_asset_assignments(
    #         model_user.userID,
    #         object_model.id
    #     )
    #     self.api_adm_users.delete_user_by_id(model_user.userID)
    #     self.api_es_assets.delete_object_by_id(object_model.id)
    #     self.api_es_companies.delete_company_by_id(company_id)
    #     self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete users asset assignments.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26056")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26056)
    def test_delete_asset_assignments(self):
        model_user = self.api_adm_users.post_add_user_staff()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        self.api_pa_asset_assignments.post_add_asset_assignments(
            model_user.userID,
            object_model.id
        )
        self.api_pa_asset_assignments.delete_asset_assignments(
            model_user.userID,
            object_model.id
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)
