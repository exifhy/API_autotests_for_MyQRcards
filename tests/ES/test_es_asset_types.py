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
class TestEsAssetTypes(BaseTest):

    @allure.title('Test get list asset types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23590")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23590)
    def test_get_list_asset_types(self):
        self.api_es_asset_types.get_all_list_asset_types()

    @allure.title('Test add asset types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23589")
    @pytest.mark.skip(reason="Тест на создание типа объекта проходит - test_delete_asset_type_by_id")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23589)
    def test_post_add_asset_types(self):
        self.api_es_asset_types.post_add_asset_types(False)

    @allure.title('Test delete asset type by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23591")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23591)
    def test_delete_asset_type_by_id(self):
        model_asset_type = self.api_es_asset_types.post_add_asset_types(False)
        self.api_es_asset_types.delete_asset_types_by_id(model_asset_type.list[0].id)

    @allure.title('Test delete asset type by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24203")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24203)
    def test_delete_asset_type_by_list(self):
        model_type = self.api_es_asset_types.post_add_asset_types(False)
        self.api_es_asset_types.delete_asset_types_by_list(model_type.list[0].id)

    @allure.title('Test get asset type by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24204")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24204)
    def test_get_asset_type_by_id(self):
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        self.api_es_asset_types.get_asset_type_by_id(asset_type_id)

    @allure.title('Test update asset types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24202")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24202)
    def test_put_update_asset_types(self):
        model_asset_type = self.api_es_asset_types.post_add_asset_types(False)
        try:
            model_before = self.api_es_asset_types.get_asset_type_by_id(model_asset_type.list[0].id)
            self.api_es_asset_types.put_update_asset_types(model_asset_type.list[0].id, False)
            model_after = self.api_es_asset_types.get_asset_type_by_id(model_asset_type.list[0].id)
            assert model_before.name != model_after.name, \
                f'{model_before.name} is equal {model_after.name}'
        finally:
            self.api_es_asset_types.delete_asset_types_by_id(model_asset_type.list[0].id)


@pytest.mark.test_scripts_suites_es_asset_types
class TestEsAssetTypesScriptSuite(BaseTest):

    @allure.title('Test api test script ES/assetTypes (POST, GET, GET by id, DELETE by list, GET, GET by id).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24567")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id(24567)
    @pytest.mark.test_script_runs
    def test_es_asset_types_add_get_get_by_id_delete_by_list_get_get_by_id(self, request, return_func_name):
        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i + 1}]")):
                try:
                    model_asset_types = self.api_es_asset_types.post_add_asset_types(True)
                    self.api_es_asset_types.get_list_asset_types(model_asset_types.list[0].id)
                    self.api_es_asset_types.get_asset_type_by_id(model_asset_types.list[0].id)
                    self.api_es_asset_types.delete_asset_types_by_list(model_asset_types.list[0].id)
                    self.api_es_asset_types.get_list_asset_types_is_deleted(model_asset_types.list[0].id)
                    self.api_es_asset_types.get_deleted_asset_type_by_id(model_asset_types.list[0].id)
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i + 1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")
        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)

    @allure.title('Test api test script ES/assetTypes (POST, GET, GET by id, DELETE by id, GET, GET by id).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24568")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id(24568)
    @pytest.mark.test_script_runs
    def test_es_asset_types_add_get_get_by_id_delete_by_id_get_get_by_id(self, request, return_func_name):
        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i + 1}]")):
                try:
                    model_asset_types = self.api_es_asset_types.post_add_asset_types(True)
                    self.api_es_asset_types.get_list_asset_types(model_asset_types.list[0].id)
                    self.api_es_asset_types.get_asset_type_by_id(model_asset_types.list[0].id)
                    self.api_es_asset_types.delete_asset_types_by_id(model_asset_types.list[0].id)
                    self.api_es_asset_types.get_list_asset_types_is_deleted(model_asset_types.list[0].id)
                    self.api_es_asset_types.get_deleted_asset_type_by_id(model_asset_types.list[0].id)
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i + 1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")
        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)

    @allure.title('Test api test script ES/assetTypes (PUT by id, GET, GET by id).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24569")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id(24569)
    @pytest.mark.test_script_runs
    def test_es_asset_types_put_get_get_by_id(self, request, return_func_name):
        model_asset_types = self.api_es_asset_types.post_add_asset_types(True)
        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with ((allure.step(f"Run #[{i + 1}]"))):
                try:
                    model_before = self.api_es_asset_types.get_asset_type_by_id(model_asset_types.list[0].id)
                    new_name_asset_types = self.api_es_asset_types.put_update_asset_types(
                        model_asset_types.list[0].id,
                        False
                    )
                    self.api_es_asset_types.get_list_asset_types_check_data_by_id(
                        new_name_asset_types,
                        model_asset_types.list[0].id)
                    model_after = self.api_es_asset_types.get_asset_type_by_id(model_asset_types.list[0].id)
                    assert model_before != model_after, \
                        f'Asset type with ID {model_asset_types.list[0].id} is not updated'
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i + 1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")

        self.api_es_asset_types.delete_asset_types_by_id(model_asset_types.list[0].id)

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)
