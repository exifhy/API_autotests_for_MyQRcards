import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Users & districts administration")
class TestAdmUserDistricts(BaseTest):

    @allure.title('Test add districts to user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23177")
    @pytest.mark.smoke
    def test_post_add_districts_to_user_customer(self):
        user_model = self.api_adm_users.post_add_user_customer()
        district_model = self.api_es_districts.post_add_district()
        self.api_adm_user_districts.post_add_districts_to_user(
            districts_id=district_model.districts[0],
            user_id=user_model.userID
        )
        self.api_adm_users.delete_user_by_id(user_model.userID)
        self.api_es_districts.delete_district_by_id(district_model.districts[0])

