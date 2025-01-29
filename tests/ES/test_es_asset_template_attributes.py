import allure
import pytest
from allure_commons.types import Severity
from loguru import logger
from requests import JSONDecodeError

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


@pytest.mark.test_scripts_suites_es_asset_template_attributes
class TestEsAssetTemplateAttributesScriptSuite(BaseTest):

    @allure.title(
        'Test script ES/assetTemplateAttributes (POST, GET, DELETE by list, GET).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id()
    @pytest.mark.test_script_runs
    def test_es_asset_template_attributes_add_get_delete_by_list_get(
            self,
            request,
            return_func_name
    ):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_template = self.api_es_asset_templates.post_add_asset_templates(
            asset_type_id, asset_class_id, location_id
        )
        attribute_id = self.api_common_attributes.post_add_method_attributes_only_for_asset_str()
        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i + 1}]")):
                try:
                    self.api_es_asset_template_attributes.post_update_attributes_asset_templates(
                        model_template.result[0],
                        attribute_id.values[0]
                    )
                    model_attribute = self.api_es_asset_templates.get_list_attributes_from_asset_template(
                        model_template.result[0],
                        False
                    )
                    assert attribute_id.values[0] == model_attribute.result[0].attribute.id, \
                        f'Attribute with ID {attribute_id.values[0]} is not in list attributes asset templates.'
                    self.api_es_asset_template_attributes.post_delete_attributes_asset_templates(
                        model_template.result[0]
                    )
                    self.api_es_asset_templates.get_list_attributes_from_asset_template(
                        model_template.result[0],
                        True
                    )
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i + 1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")

        self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])
        self.api_es_locations.delete_location_by_id(location_id)
        self.api_common_attributes.delete_method_attribute_by_id(attribute_id.values[0])

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)
