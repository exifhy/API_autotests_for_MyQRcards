import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmUserTags(BaseTest):

    @allure.title('Test add tags to user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26145")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26145)
    def test_post_add_tags_to_user(self):
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_adm_user_tags.post_add_tags_to_user(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test delete tags from user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26146")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26146)
    def test_delete_tags_from_user(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_tags = self.api_adm_user_tags.post_add_tags_to_user(model_user.userID)
        self.api_adm_user_tags.delete_tags_from_user(
            model_tags.results[0].userID,
            model_tags.results[0].tag
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
