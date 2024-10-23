import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Actions with the locations")
class TestLocations(BaseTest):

    @pytest.mark.skip(reason='Location is created in test - test_delete_location_by_id.')
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23060)
    @allure.title('Test add location.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23060")
    def test_post_add_location(self):
        self.api_es_locations.post_add_location()

    @allure.title('Test delete location by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23063")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23063)
    def test_delete_location_by_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        self.api_es_locations.delete_location_by_id(location_id=created_location_id)


