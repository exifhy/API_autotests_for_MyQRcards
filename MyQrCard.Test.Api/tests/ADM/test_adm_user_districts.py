import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Users & districts administration")
class TestAdmUserDistricts(BaseTest):

    @allure.title('Test add districts to user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23177")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23177)
    def test_post_add_districts_to_user_customer(self):
        user_model = self.api_adm_users.post_add_user_customer()
        district_model = self.api_es_districts.post_add_district()
        self.api_adm_user_districts.post_add_districts_to_user(
            districts_id=district_model.districts[0],
            user_id=user_model.userID
        )
        self.api_adm_users.delete_user_by_id(user_model.userID)
        self.api_es_districts.delete_district_by_id(district_model.districts[0])

    @allure.title('Test delete users districts.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26021")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26021)
    def test_delete_districts_from_user(self):
        user_model = self.api_adm_users.post_add_user_customer()
        district_model = self.api_es_districts.post_add_three_districts()
        self.api_adm_user_districts.post_add_three_districts_to_user(
            user_model.userID, district_model
        )
        self.api_adm_user_districts.delete_districts_from_user(
            user_model.userID,
            district_model.districts[0],
            district_model.districts[1],
            district_model.districts[2]
        )
        self.api_adm_users.delete_user_by_id(user_model.userID)
        self.api_es_districts.delete_districts_by_list(
            district_model.districts[0],
            district_model.districts[1],
            district_model.districts[2]
        )

    @allure.title('Test update districts user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26022")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26022)
    def test_put_update_districts_user(self):
        user_model = self.api_adm_users.post_add_user_customer()
        district_model = self.api_es_districts.post_add_three_districts()
        self.api_adm_user_districts.post_add_three_districts_to_user(
            user_model.userID, district_model
        )
        self.api_adm_user_districts.put_update_districts_user(
            user_model.userID, district_model
        )
        self.api_adm_users.delete_user_by_id(user_model.userID)
        self.api_es_districts.delete_districts_by_list(
            district_model.districts[0],
            district_model.districts[1],
            district_model.districts[2]
        )
