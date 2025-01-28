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


@pytest.mark.test_scripts_suites_es_asset_template_work_types
class TestEsAssetTemplateWorkTypesScriptSuite(BaseTest):

    @allure.title('Test script ES/assetTemplateWorkTypes (POST, GET, DELETE by list, GET).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id()
    @pytest.mark.test_script_runs
    def test_es_asset_template_work_types_add_get_delete_by_list_get(self, request, return_func_name):
        model_template = self.api_es_asset_templates.post_add_empty_asset_template()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()

        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i + 1}]")):
                try:
                    self.api_es_asset_template_work_types.post_add_work_types_to_asset_templates(
                        model_template.result[0],
                        work_type_id
                    )
                    model_get_list_work_types = self.api_es_asset_templates.get_list_work_types_from_asset_templates(
                        model_template.result[0],
                        False
                    )
                    assert work_type_id == model_get_list_work_types.result[0].workType.id, \
                        f'Work type with ID {work_type_id} is not in list asset template work types'
                    self.api_es_asset_template_work_types.delete_work_types_from_asset_templates(
                        model_template.result[0],
                        work_type_id
                    )
                    self.api_es_asset_templates.get_list_work_types_from_asset_templates(
                        model_template.result[0],
                        True
                    )
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i + 1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")

        self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)
