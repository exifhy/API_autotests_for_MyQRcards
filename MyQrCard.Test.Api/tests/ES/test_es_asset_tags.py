import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestEsAssetTags(BaseTest):

    # @allure.title('Test add add tags to the asset.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24125")
    # @pytest.mark.skip(reason="Тест на создания тэга проходит в - test_delete_tags_from_asset")
    # @pytest.mark.regress
    # @pytest.mark.test_case_id(24125)
    # def test_post_add_tags_to_asset(self):
    #     company_id = self.api_es_companies.post_add_our_company()
    #     location_id = self.api_es_locations.post_add_location()
    #     self.api_es_company_locations.post_add_company_locations(
    #         company_id=company_id,
    #         location_id=location_id
    #     )
    #     asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
    #     asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
    #     model_asset = self.api_es_assets.post_add_object(
    #         company_id=company_id,
    #         asset_class_id=asset_class_id,
    #         asset_type_id=asset_type_id
    #     )
    #     try:
    #         self.api_es_asset_tags.post_add_tags_to_asset(model_asset.id)
    #     finally:
    #         self.api_es_assets.delete_object_by_id(model_asset.id)
    #         self.api_es_companies.delete_company_by_id(company_id)
    #         self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete tags from the asset.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24126")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24126)
    def test_delete_tags_from_asset(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            model_tags = self.api_es_asset_tags.post_add_tags_to_asset(model_asset.id)
            self.api_es_asset_tags.delete_tags_from_asset(
                model_asset.id,
                model_tags.result[0].tag
            )
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
