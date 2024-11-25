import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestEsAssetSkills(BaseTest):

    @allure.title('Test add skills to assets.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24015")
    @pytest.mark.skip(reason="Тест на добавление навыка к объекту проходит в test_delete_skills_from_one_asset(24017)")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24015)
    def test_post_add_skills_to_one_asset(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_skills = self.api_pa_skills.post_add_three_skills_to_tenant()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            self.api_es_asset_skills.post_add_skills_to_one_asset(
                model_asset.id,
                model_skills.skills[0].skillID,
                model_skills.skills[1].skillID,
                model_skills.skills[2].skillID
            )
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_locations_by_list(location_id)
            self.api_pa_skills.delete_skills_by_list(
                model_skills.skills[0].skillID,
                model_skills.skills[1].skillID,
                model_skills.skills[2].skillID
            )

    @allure.title('Test delete skills from assets.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24017")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24017)
    def test_delete_skills_from_one_asset(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_skills = self.api_pa_skills.post_add_three_skills_to_tenant()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )

        try:
            self.api_es_asset_skills.post_add_skills_to_one_asset(
                model_asset.id,
                model_skills.skills[0].skillID,
                model_skills.skills[1].skillID,
                model_skills.skills[2].skillID
            )
            self.api_es_asset_skills.delete_skills_from_one_asset(
                model_asset.id,
                model_skills.skills[0].skillID,
                model_skills.skills[1].skillID,
                model_skills.skills[2].skillID
            )
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_locations_by_list(location_id)
            self.api_pa_skills.delete_skills_by_list(
                model_skills.skills[0].skillID,
                model_skills.skills[1].skillID,
                model_skills.skills[2].skillID
            )