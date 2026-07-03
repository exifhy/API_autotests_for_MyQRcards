import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmInvitations(BaseTest):

    @allure.title('Test get list invitation.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25808")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25808)
    def test_get_list_invitation(self):
        self.api_adm_invitations.get_list_invitation()

    @allure.title('Test add invitation.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25809")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25809)
    def test_post_add_invitation(self):
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_invitation = self.api_adm_invitations.post_add_invitation(model_template.results[0])
        self.api_adm_invitations.delete_invitations_by_list(model_invitation.results[0].id)
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test get invitation by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25810")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25810)
    def test_get_invitation_by_id(self):
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_invitation = self.api_adm_invitations.post_add_invitation(model_template.results[0])
        self.api_adm_invitations.get_invitation_by_id(model_invitation.results[0].id)
        self.api_adm_invitations.delete_invitations_by_list(model_invitation.results[0].id)
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test delete invitation by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25811")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25811)
    @pytest.mark.xfail(reason="https://dev.azure.com/melston/HubEx/_workitems/edit/25821")
    def test_delete_invitation_by_id(self):
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_invitation = self.api_adm_invitations.post_add_invitation(model_template.results[0])
        try:
            self.api_adm_invitations.delete_invitation_by_id(model_invitation.results[0].id)
        finally:
            self.api_adm_invitations.delete_invitations_by_list(model_invitation.results[0].id)
            self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test get short invitation by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25812")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25812)
    def test_get_short_invitation_by_id(self):
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_invitation = self.api_adm_invitations.post_add_invitation(model_template.results[0])
        self.api_adm_invitations.get_short_invitation_by_id(model_invitation.results[0].id)
        self.api_adm_invitations.delete_invitations_by_list(model_invitation.results[0].id)
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test update invitation.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25813")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25813)
    def test_put_update_invitation(self):
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_invitation = self.api_adm_invitations.post_add_invitation(model_template.results[0])
        self.api_adm_invitations.put_update_invitation(
            model_invitation.results[0].id,
            model_template.results[0]
        )
        self.api_adm_invitations.delete_invitations_by_list(model_invitation.results[0].id)
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test delete invitations by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25814")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25814)
    def test_delete_invitations_by_list(self):
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_invitation = self.api_adm_invitations.post_add_three_invitations(model_template.results[0])
        self.api_adm_invitations.delete_invitations_by_list(
            model_invitation.results[0].id,
            model_invitation.results[1].id,
            model_invitation.results[2].id
        )
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])
