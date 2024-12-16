import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestEsAssetTemplateWorkTypes(BaseTest):

    @allure.title('Test add work types to asset templates.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24163")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24163)
    def test_post_add_work_types_to_asset_templates(self):
        model_template = self.api_es_asset_templates.post_add_empty_asset_template()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        self.api_es_asset_template_work_types.post_add_work_types_to_asset_templates(
            model_template.result[0],
            work_type_id
        )
        self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])

    @allure.title('Test delete work types from asset templates.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24187")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24187)
    def test_delete_work_types_from_asset_templates(self):
        model_template = self.api_es_asset_templates.post_add_empty_asset_template()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        self.api_es_asset_template_work_types.post_add_work_types_to_asset_templates(
            model_template.result[0],
            work_type_id
        )
        self.api_es_asset_template_work_types.delete_work_types_from_asset_templates(
            model_template.result[0],
            work_type_id
        )
        self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])

    @allure.title('Test delete work types from asset template by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24188")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24188)
    def test_delete_work_types_from_asset_template_by_id(self):
        model_template = self.api_es_asset_templates.post_add_empty_asset_template()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        self.api_es_asset_template_work_types.post_add_work_types_to_asset_templates(
            model_template.result[0],
            work_type_id
        )
        self.api_es_asset_template_work_types.delete_work_types_from_asset_template_by_id(
            model_template.result[0],
            work_type_id
        )
        self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])
