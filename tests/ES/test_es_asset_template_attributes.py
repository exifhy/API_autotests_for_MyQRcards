import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestEsAssetTemplateAttributes(BaseTest):

    @allure.title('Test update attributes asset templates.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24167")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24167)
    def test_post_update_attributes_asset_templates(self):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_template = self.api_es_asset_templates.post_add_asset_templates(
            asset_type_id, asset_class_id, location_id
        )
        attribute_id = self.api_common_attributes.post_add_method_attributes_only_for_asset_str()
        try:
            self.api_es_asset_template_attributes.post_update_attributes_asset_templates(
                model_template.result[0],
                attribute_id.values[0]
            )
        finally:
            self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_attributes.delete_method_attribute_by_id(attribute_id=attribute_id.values[0])
