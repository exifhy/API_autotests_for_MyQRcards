import allure
import pytest
from allure_commons.types import Severity
from loguru import logger
from pydantic_core import ValidationError
from requests import JSONDecodeError

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


@pytest.mark.test_scripts_suites_es_asset_template_skills
class TestEsAssetTemplateSkillsScriptSuite(BaseTest):

    @allure.title(
        'Test script ES/assetTemplateSkills (POST, GET, DELETE by list, GET).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id()
    @pytest.mark.test_script_runs
    @pytest.mark.xfail(reason="get_list_skills_from_asset_templates -> 500. Unable To Resolve")
    def test_es_asset_template_skills_add_get_delete_by_list_get(
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
        skill_id = self.api_pa_skills.post_add_skills_to_tenant()

        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i + 1}]")):
                try:
                    self.api_es_asset_template_skills.post_skills_to_asset_templates(
                        model_template.result[0],
                        skill_id.skills[0].skillID
                    )
                    model_get_list_skills = self.api_es_asset_templates.get_list_skills_from_asset_templates(
                        model_template.result[0],
                        False
                    )
                    assert skill_id.skills[0].skillID in model_get_list_skills.result, \
                        f'Skills with ID {skill_id.skills[0].skillID} is not in list skills asset templates.'
                    self.api_es_asset_template_skills.delete_skills_from_asset_templates(
                        model_template.result[0],
                        skill_id.skills[0].skillID
                    )
                    self.api_es_asset_templates.get_list_skills_from_asset_templates(
                        model_template.result[0],
                        True
                    )
                except (AssertionError, JSONDecodeError, ValidationError) as e:
                    logger.error(f"Error in Run #[{i + 1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")

        self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])
        self.api_es_locations.delete_location_by_id(location_id)
        self.api_pa_skills.delete_skill_by_id(skill_id.skills[0].skillID)

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)

    @allure.title(
        'Test script ES/assetTemplateSkills (POST, GET, DELETE by id, GET).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id()
    @pytest.mark.test_script_runs
    @pytest.mark.xfail(reason="get_list_skills_from_asset_templates -> 500. Unable To Resolve")
    def test_es_asset_template_skills_add_get_delete_by_id_get(
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
        skill_id = self.api_pa_skills.post_add_skills_to_tenant()

        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i + 1}]")):
                try:
                    self.api_es_asset_template_skills.post_skills_to_asset_templates(
                        model_template.result[0],
                        skill_id.skills[0].skillID
                    )
                    model_get_list_skills = self.api_es_asset_templates.get_list_skills_from_asset_templates(
                        model_template.result[0],
                        False
                    )
                    assert skill_id.skills[0].skillID in model_get_list_skills.result, \
                        f'Skills with ID {skill_id.skills[0].skillID} is not in list skills asset templates.'
                    self.api_es_asset_template_skills.delete_skills_from_asset_template_by_id(
                        model_template.result[0],
                        skill_id.skills[0].skillID
                    )
                    self.api_es_asset_templates.get_list_skills_from_asset_templates(
                        model_template.result[0],
                        True
                    )
                except (AssertionError, JSONDecodeError, ValidationError) as e:
                    logger.error(f"Error in Run #[{i + 1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")

        self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])
        self.api_es_locations.delete_location_by_id(location_id)
        self.api_pa_skills.delete_skill_by_id(skill_id.skills[0].skillID)

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)
