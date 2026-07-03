import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestEsAssetAttributes(BaseTest):

    @allure.title('Test update assets attributes.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23809")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23809)
    def test_post_update_attributes_assets(self):
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
        attribute_id = self.api_common_attributes.post_add_method_attributes_only_for_asset_str()
        try:
            self.api_es_asset_attributes.post_update_attributes_assets(
                asset_id=model_asset.id,
                attribute_id=attribute_id.values[0]
            )
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_attributes.delete_method_attribute_by_id(attribute_id=attribute_id.values[0])


