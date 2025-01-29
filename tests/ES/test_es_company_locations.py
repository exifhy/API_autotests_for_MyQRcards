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
class TestEsCompanyLocations(BaseTest):

    @allure.title('Test add a location to the company.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23558")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23558)
    def test_add_location_to_company(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        try:
            self.api_es_company_locations.post_add_company_locations(company_id, location_id)
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test update location by company.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24274")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24274)
    def test_put_update_location_by_company(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id_first = self.api_es_locations.post_add_location()
        location_id_second = self.api_es_locations.post_add_location()
        try:
            self.api_es_company_locations.post_add_company_locations(company_id, location_id_first)
            self.api_es_company_locations.put_update_location_from_company(company_id, location_id_second)
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_locations_by_list(location_id_first, location_id_second)

    @allure.title('Test get location from company by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24273")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24273)
    def test_get_location_from_company_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        try:
            self.api_es_company_locations.post_add_company_locations(company_id, location_id)
            self.api_es_company_locations.get_list_locations_company(company_id)
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete location from company by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24275")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24275)
    def test_delete_location_from_company_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        try:
            self.api_es_company_locations.post_add_company_locations(company_id, location_id)
            self.api_es_company_locations.delete_location_from_company(company_id)
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)


@pytest.mark.test_scripts_suites_es_company_locations
class TestEsCompanyLocationsScriptSuite(BaseTest):

    @allure.title('Test script ES/companyLocations (POST, GET, DELETE by list, GET).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id()
    @pytest.mark.test_script_runs
    def test_es_company_locations_add_get_delete_by_list_get(self, request, return_func_name):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i + 1}]")):
                try:
                    self.api_es_company_locations.post_add_company_locations(company_id, location_id)
                    model_list_locations = self.api_es_company_locations.get_list_locations_company_with_asserts(
                        company_id,
                        location_id,
                        False
                    )
                    self.api_es_companies.get_company_by_id_assert_location(
                        company_id,
                        model_list_locations.root[str(location_id)],
                        False
                    )
                    self.api_es_company_locations.delete_location_from_company(company_id)
                    self.api_es_company_locations.get_list_locations_company_with_asserts(
                        company_id,
                        location_id,
                        True
                    )
                    self.api_es_companies.get_company_by_id_assert_location(
                        company_id,
                        model_list_locations.root[str(location_id)],
                        True
                    )
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i + 1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")

        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)
