import allure
import pytest
from config.base_test import BaseTest
from src.enums.params_enums import Params


@allure.epic("Administration")
@allure.feature("Actions with the object")
class TestEsAssets(BaseTest):

    @allure.title('Test returns the directory of objects available to the user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23025")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23025)
    @pytest.mark.parametrize('param', Params.params_assets_list.value)
    def test_get_directory_of_objects_available_to_user(self, param):
        self.api_es_assets.get_directory_of_objects_available_to_user(param)

    @pytest.mark.smoke
    @pytest.mark.skip(reason='Object is created in test - test_delete_object_by_id.')
    @pytest.mark.test_case_id(23026)
    @allure.title('Test object creation.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23026")
    def test_post_add_object(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        self.api_es_assets.post_add_object(company_id)

    @allure.title('Test marks the object as remote.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23027")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23027)
    def test_delete_object_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        model = self.api_es_assets.post_add_object(company_id)
        self.api_es_assets.delete_object_by_id(model.id)
        self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test detailed information on the object by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23031")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23031)
    def test_get_detailed_information_on_object_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        model = self.api_es_assets.post_add_object(company_id)
        self.api_es_assets.get_detailed_information_on_object_by_id(model.id)
        self.api_es_assets.delete_object_by_id(model.id)
        self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test object publication.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23078")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23078)
    def test_put_method_of_publishing_an_object_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        created_location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
        )
        object_model = self.api_es_assets.post_add_object(company_id)
        self.api_es_assetlocations.add_location_to_object(
            asset_id=object_model.id,
            location_id=created_location_id
        )
        self.api_es_assets.put_method_of_publishing_an_object_by_id(object_model.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test object publication without location.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23084")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23084)
    def test_put_method_of_publishing_an_object_by_id_without_location(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        object_model = self.api_es_assets.post_add_object(company_id)
        self.api_es_assets.put_method_of_publishing_an_object_by_id_without_location(object_model.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test update the object by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23080")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23080)
    def test_put_update_object_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        object_model = self.api_es_assets.post_add_object(company_id)
        self.api_es_assets.put_update_object_by_id(object_model.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
