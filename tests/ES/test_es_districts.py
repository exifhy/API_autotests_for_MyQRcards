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
class TestEsDistricts(BaseTest):

    @pytest.mark.smoke
    @pytest.mark.test_case_id(23087)
    @pytest.mark.skip(reason='District is created in test - test_delete_district_by_id.')
    @allure.title('Test add district.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23087")
    def test_post_add_district(self):
        self.api_es_districts.post_add_district()

    @allure.title('Test delete the district.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23088")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23088)
    def test_delete_district_by_id(self):
        district_id = self.api_es_districts.post_add_district()
        self.api_es_districts.delete_district_by_id(district_id=district_id.districts[0])

    @allure.title('Test get list districts.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24289")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24289)
    def test_get_list_districts(self):
        self.api_es_districts.get_list_districts()

    @allure.title('Test get districts by ID')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23186")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23186)
    def test_get_district_by_id(self):
        district_id = self.api_es_districts.post_add_district()
        self.api_es_districts.get_detail_district_info_by_id(district_id.districts[0])

    @allure.title('Test get districts by ID')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23998")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23998)
    def test_delete_districts_by_list(self):
        district_id_first = self.api_es_districts.post_add_district()
        district_id_second = self.api_es_districts.post_add_district()
        district_id_third = self.api_es_districts.post_add_district()
        self.api_es_districts.delete_districts_by_list(
            district_id_first.districts[0],
            district_id_second.districts[0],
            district_id_third.districts[0],
        )

    @allure.title('Test update district.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24290")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24290)
    def test_put_update_district(self):
        district_id = self.api_es_districts.post_add_district()
        district_before = self.api_es_districts.get_detail_district_info_by_id(district_id.districts[0])
        self.api_es_districts.put_update_district(district_id.districts[0])
        district_after = self.api_es_districts.get_detail_district_info_by_id(district_id.districts[0])
        assert district_before != district_after, f'{district_before} is equal {district_after}'
        self.api_es_districts.delete_district_by_id(district_id.districts[0])

    @allure.title('Test update parent district.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24291")
    @pytest.mark.skip(reason="Ручка не используется, описана на будущее.")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24291)
    def test_put_update_parent_district(self):
        pass

    @allure.title('Test update district sorted.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24292")
    @pytest.mark.skip(reason="Ручка не используется, описана на будущее.")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24292)
    def test_put_update_district_sorted(self):
        pass


@pytest.mark.test_scripts_suites_es_districts
class TestEsDistrictsScriptSuite(BaseTest):

    @allure.title('Test script ES/districts (POST, GET, PUT, GET, DELETE by id, GET).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id()
    @pytest.mark.test_script_runs
    def test_es_districts_add_get_put_get_delete_by_id_get(self, request, return_func_name):
        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i + 1}]")):
                try:
                    district_id = self.api_es_districts.post_add_district()
                    model_before = self.api_es_districts.get_list_districts_with_asserts(district_id.districts[0], False)
                    self.api_es_districts.put_update_district(district_id.districts[0])
                    model_after = self.api_es_districts.get_list_districts()
                    assert model_before != model_after, f'{model_before} is equal {model_after}'
                    self.api_es_districts.delete_district_by_id(district_id.districts[0])
                    self.api_es_districts.get_list_districts_with_asserts(district_id.districts[0], True)
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i + 1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)
