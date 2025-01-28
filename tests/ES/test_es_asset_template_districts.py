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


@pytest.mark.test_scripts_suites_es_asset_template_districts
class TestEsAssetTemplateDistrictsScriptSuite(BaseTest):

    @allure.title(
        'Test script ES/assetTemplateDistricts (POST, GET, DELETE by list, GET).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id()
    def test_es_asset_template_districts_add_get_delete_by_list_get(
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
        district_id = self.api_es_districts.post_add_district()
        model_district = self.api_es_districts.get_detail_district_info_by_id(district_id.districts[0])
        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i + 1}]")):
                try:
                    self.api_es_asset_template_districts.post_districts_to_asset_templates(
                        model_template.result[0],
                        district_id.districts[0]
                    )
                    model_get_list_districts = self.api_es_asset_templates.get_list_districts_from_asset_templates(
                        model_template.result[0],
                        False
                    )
                    assert str(model_district.id) in model_get_list_districts.root, \
                        f'District asset template with ID {model_district.id} is not in list template districts'
                    assert model_district.name == model_get_list_districts.root[str(model_district.id)].name, \
                        f'District asset template with name {model_district.name} is not in list template districts'
                    self.api_es_asset_template_districts.delete_districts_from_asset_templates(
                        model_template.result[0],
                        district_id.districts[0]
                    )
                    self.api_es_asset_templates.get_list_districts_from_asset_templates(
                        model_template.result[0],
                        True
                    )
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i + 1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")

        self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])
        self.api_es_locations.delete_location_by_id(location_id)
        self.api_es_districts.delete_district_by_id(district_id.districts[0])

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)

    @allure.title(
        'Test script ES/assetTemplateDistricts (POST, GET, DELETE by ID, GET).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id()
    def test_es_asset_template_districts_add_get_delete_by_id_get(
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
        district_id = self.api_es_districts.post_add_district()
        model_district = self.api_es_districts.get_detail_district_info_by_id(district_id.districts[0])
        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i + 1}]")):
                try:
                    self.api_es_asset_template_districts.post_districts_to_asset_templates(
                        model_template.result[0],
                        district_id.districts[0]
                    )
                    model_get_list_districts = self.api_es_asset_templates.get_list_districts_from_asset_templates(
                        model_template.result[0],
                        False
                    )
                    assert str(model_district.id) in model_get_list_districts.root, \
                        f'District asset template with ID {model_district.id} is not in list template districts'
                    assert model_district.name == model_get_list_districts.root[str(model_district.id)].name, \
                        f'District asset template with name {model_district.name} is not in list template districts'
                    self.api_es_asset_template_districts.delete_districts_from_asset_template_by_id(
                        model_template.result[0],
                        district_id.districts[0]
                    )
                    self.api_es_asset_templates.get_list_districts_from_asset_templates(
                        model_template.result[0],
                        True
                    )
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i + 1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")

        self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])
        self.api_es_locations.delete_location_by_id(location_id)
        self.api_es_districts.delete_district_by_id(district_id.districts[0])

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)
