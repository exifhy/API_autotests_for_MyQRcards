import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestLocations(BaseTest):

    @pytest.mark.skip(reason='Location is created in test - test_delete_location_by_id.')
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23060)
    @allure.title('Test add location.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23060")
    def test_post_add_location(self):
        self.api_es_locations.post_add_location()

    @pytest.mark.regress
    @pytest.mark.test_case_id(24293)
    @allure.title('Test get list locations.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24293")
    def test_get_list_locations(self):
        self.api_es_locations.get_list_locations()

    @allure.title('Test delete location by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24298")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(24298)
    def test_delete_location_by_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        self.api_es_locations.delete_location_by_id(location_id=created_location_id)

    @allure.title('Test delete location by ID (remove).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23063")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23063)
    def test_delete_location_by_id_remove(self):
        created_location_id = self.api_es_locations.post_add_location()
        self.api_es_locations.delete_location_by_id_remove(location_id=created_location_id)

    @allure.title('Test delete location by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23991")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23991)
    def test_delete_locations_by_list(self):
        location_id_first = self.api_es_locations.post_add_location()
        location_id_second = self.api_es_locations.post_add_location()
        location_id_third = self.api_es_locations.post_add_location()
        self.api_es_locations.delete_locations_by_list(
            location_id_first,
            location_id_second,
            location_id_third
        )

    @allure.title('Test delete location by list (remove).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24299")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24299)
    def test_delete_locations_by_list_remove(self):
        location_id_first = self.api_es_locations.post_add_location()
        location_id_second = self.api_es_locations.post_add_location()
        location_id_third = self.api_es_locations.post_add_location()
        self.api_es_locations.delete_location_by_list_remove(
            location_id_first,
            location_id_second,
            location_id_third
        )

    @allure.title('Test update location.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24294")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24294)
    def test_put_update_location(self):
        location_id = self.api_es_locations.post_add_location()
        try:
            self.api_es_locations.put_update_location(location_id)
        finally:
            self.api_es_locations.delete_location_by_id_remove(location_id)

    @allure.title('Test get location by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24297")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24297)
    def test_get_location_by_id(self):
        location_id = self.api_es_locations.post_add_location()
        self.api_es_locations.get_location_by_id(location_id)
        self.api_es_locations.delete_location_by_id_remove(location_id)
