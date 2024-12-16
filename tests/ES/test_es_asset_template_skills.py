import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestEsAssetTemplateSkills(BaseTest):

    @allure.title('Test add skills to asset templates.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24184")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24184)
    def test_post_skills_to_asset_templates(self):
        skill_id = self.api_pa_skills.get_list_skills_tenant_return_first_skills()
        model_template = self.api_es_asset_templates.post_add_empty_asset_template()
        self.api_es_asset_template_skills.post_skills_to_asset_templates(
            model_template.result[0],
            skill_id
        )
        self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])

    @allure.title('Test delete skills from asset templates.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24185")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24185)
    def test_delete_skills_from_asset_templates(self):
        skill_id = self.api_pa_skills.get_list_skills_tenant_return_first_skills()
        model_template = self.api_es_asset_templates.post_add_empty_asset_template()
        self.api_es_asset_template_skills.post_skills_to_asset_templates(
            model_template.result[0],
            skill_id
        )
        self.api_es_asset_template_skills.delete_skills_from_asset_templates(
            model_template.result[0],
            skill_id
        )
        self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])

    @allure.title('Test delete skills from asset template by Id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24186")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24186)
    def test_delete_skills_from_asset_template_by_id(self):
        skill_id = self.api_pa_skills.get_list_skills_tenant_return_first_skills()
        model_template = self.api_es_asset_templates.post_add_empty_asset_template()
        self.api_es_asset_template_skills.post_skills_to_asset_templates(
            model_template.result[0],
            skill_id
        )
        self.api_es_asset_template_skills.delete_skills_from_asset_template_by_id(
            model_template.result[0],
            skill_id
        )
        self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])
