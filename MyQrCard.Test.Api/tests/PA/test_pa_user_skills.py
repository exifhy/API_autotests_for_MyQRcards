import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Service offers application programming interface for manipulation personnel and all connected entities."
)
class TestPaUserSkills(BaseTest):

    @allure.title('Test add skills to user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26114")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26114)
    def test_post_add_skills_to_user(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_skills = self.api_pa_skills.post_add_skills_to_tenant()
        self.api_pa_user_skills.post_add_skills_to_user(
            model_user.userID,
            model_skills.skills[0].skillID
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_pa_skills.delete_skill_by_id(model_skills.skills[0].skillID)

    @allure.title('Test update user skills.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26115")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26115)
    @pytest.mark.skip(reason="PUT не отрабатывает.")
    def test_put_update_user_skills(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_skills = self.api_pa_skills.post_add_skills_to_tenant()
        self.api_pa_user_skills.post_add_skills_to_user(
            model_user.userID,
            model_skills.skills[0].skillID
        )
        self.api_pa_user_skills.put_update_user_skills(
            model_user.userID,
            model_skills.skills[0].skillID
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_pa_skills.delete_skill_by_id(model_skills.skills[0].skillID)

    @allure.title('Test delete skills from user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26116")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26116)
    def test_delete_skills_from_user(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_skills = self.api_pa_skills.post_add_skills_to_tenant()
        self.api_pa_user_skills.post_add_skills_to_user(
            model_user.userID,
            model_skills.skills[0].skillID
        )
        self.api_pa_user_skills.delete_skills_from_user(
            model_user.userID,
            model_skills.skills[0].skillID
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_pa_skills.delete_skill_by_id(model_skills.skills[0].skillID)
