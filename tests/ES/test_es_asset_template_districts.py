import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestEsAssetTemplateDistricts(BaseTest):

    @allure.title('Test add districts to asset templates.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24157")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24157)
    def test_post_districts_to_asset_templates(self):
        district_id = self.api_es_districts.post_add_district()
        model_template = self.api_es_asset_templates.post_add_empty_asset_template()
        self.api_es_asset_template_districts.post_districts_to_asset_templates(
            model_template.result[0],
            district_id.districts[0]
        )
        self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])
        self.api_es_districts.delete_district_by_id(district_id.districts[0])

    @allure.title('Test delete districts from asset templates.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24189")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24189)
    def test_delete_districts_from_asset_templates(self):
        district_id = self.api_es_districts.post_add_district()
        model_template = self.api_es_asset_templates.post_add_empty_asset_template()
        self.api_es_asset_template_districts.post_districts_to_asset_templates(
            model_template.result[0],
            district_id.districts[0]
        )
        self.api_es_asset_template_districts.delete_districts_from_asset_templates(
            model_template.result[0],
            district_id.districts[0]
        )
        self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])
        self.api_es_districts.delete_district_by_id(district_id.districts[0])

    @allure.title('Test delete districts from asset template by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24190")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24190)
    def test_delete_districts_from_asset_template_by_id(self):
        district_id = self.api_es_districts.post_add_district()
        model_template = self.api_es_asset_templates.post_add_empty_asset_template()
        self.api_es_asset_template_districts.post_districts_to_asset_templates(
            model_template.result[0],
            district_id.districts[0]
        )
        self.api_es_asset_template_districts.delete_districts_from_asset_template_by_id(
            model_template.result[0],
            district_id.districts[0]
        )
        self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])
        self.api_es_districts.delete_district_by_id(district_id.districts[0])
