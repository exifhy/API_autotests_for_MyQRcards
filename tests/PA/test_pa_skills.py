import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Service offers application programming interface for manipulation personnel and all connected entities."
)
class TestPaSkills(BaseTest):

    @allure.title('Test add skills to this tenant.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24008")
    @pytest.mark.skip(reason="Тест на создание навыка проходит в - test_delete_skill_by_id")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24008)
    def test_post_add_skills_to_tenant(self):
        self.api_pa_skills.post_add_skills_to_tenant()

    @allure.title('Test delete skill by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24013")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24013)
    def test_delete_skill_by_id(self):
        model_skill = self.api_pa_skills.post_add_skills_to_tenant()
        self.api_pa_skills.delete_skill_by_id(model_skill.skills[0].skillID)

    @allure.title('Test get the list of skills for the given tenant.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24009")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24009)
    def test_get_list_skills_tenant(self):
        self.api_pa_skills.get_list_skills_tenant()

    @allure.title('Test get skill by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24012")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24012)
    def test_get_skill_by_id(self):
        model_skill = self.api_pa_skills.post_add_skills_to_tenant()
        try:
            self.api_pa_skills.get_skill_by_id(model_skill.skills[0].skillID)
        finally:
            self.api_pa_skills.delete_skill_by_id(model_skill.skills[0].skillID)

    @allure.title('Test update skills to this tenant.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24010")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24010)
    def test_put_update_skills_to_tenant(self):
        model_skill = self.api_pa_skills.post_add_skills_to_tenant()
        model_skill_before = self.api_pa_skills.get_skill_by_id(model_skill.skills[0].skillID)
        self.api_pa_skills.put_update_skills_to_tenant(model_skill.skills[0].skillID)
        model_skill_after = self.api_pa_skills.get_skill_by_id(model_skill.skills[0].skillID)
        assert model_skill_before.name != model_skill_after.name, \
            f'{model_skill_before.name} is equal {model_skill_after.name}'
        assert model_skill_before.description != model_skill_after.description, \
            f'{model_skill_before.description} is equal {model_skill_after.description}'
        self.api_pa_skills.delete_skill_by_id(model_skill.skills[0].skillID)

    @allure.title('Test delete skills by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24011")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24011)
    def test_delete_skills_by_list(self):
        model_skill = self.api_pa_skills.post_add_three_skills_to_tenant()
        self.api_pa_skills.delete_skills_by_list(
            model_skill.skills[0].skillID,
            model_skill.skills[1].skillID,
            model_skill.skills[2].skillID
        )
