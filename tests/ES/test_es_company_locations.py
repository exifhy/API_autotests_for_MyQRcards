import allure
import pytest
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
