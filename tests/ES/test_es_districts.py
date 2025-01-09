import allure
import pytest
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
