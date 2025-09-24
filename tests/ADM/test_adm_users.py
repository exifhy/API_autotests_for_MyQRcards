import os
import allure
import pytest
from config.base_test import BaseTest
from src.enums.params_enums import Params


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
@pytest.mark.xdist_group(name="many_users")
class TestAdmUsers(BaseTest):

    @allure.title('Test add new user customer.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23168")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23168)
    def test_post_add_user_customer(self):
        self.api_adm_users.post_add_user_customer()

    @allure.title('Test add new user staff.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23169")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23169)
    def test_post_add_user_staff(self):
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test get list users info.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23272")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23272)
    def test_get_list_users_info(self):
        self.api_adm_users.get_list_users_info()

    @allure.title('Test get detail user info by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23185")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23185)
    def test_get_user_info_by_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.get_user_info_by_id(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test update user by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23286")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23286)
    def test_put_update_user_by_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_info_user = self.api_adm_users.get_user_info_by_id(model_user.userID)
        self.api_adm_users.put_update_user_by_id(
            user_id=model_user.userID,
            user_email=model_info_user.email,
            user_phone=model_info_user.mobilePhone
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test get users roles by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23554")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23554)
    def test_get_users_roles_by_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_roles = self.api_adm_roles.get_list_roles_undeleted()
        self.api_adm_user_roles.post_add_roles_to_user(model_user.userID, model_roles.results[0].id)
        self.api_adm_users.get_users_roles_by_id(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test get a list asset queries to the current user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23883")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23883)
    def test_get_list_asset_queries_to_current_user(self, bearer_token):
        self.api_adm_users.get_list_asset_queries_to_current_user(bearer_token)

    @allure.title('Test delete users by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26160")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26160)
    def test_delete_users_by_list(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_user2 = self.api_adm_users.post_add_user_staff()
        model_user3 = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.delete_users_by_list(
            model_user.userID,
            model_user2.userID,
            model_user3.userID,
        )

    @allure.title('Test get user asset assignments by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26048")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26048)
    def test_get_user_asset_assignments_by_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        self.api_pa_asset_assignments.post_add_asset_assignments(
            model_user.userID,
            object_model.id
        )
        self.api_adm_users.get_user_asset_assignments_by_id(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get user asset list queries by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26069")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26069)
    def test_get_user_asset_list_queries_by_id(self, bearer_token):
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        tenant_id = self.api_adm_tenants.get_data_current_tenant()
        model_user = self.api_adm_users.post_add_user_customer()
        model_queries = self.api_es_asset_list_queries.post_add_asset_list_queries_only_asset_type(
            bearer_token, asset_type_id, tenant_id.uriName
        )
        try:
            self.api_adm_user_asset_list_queries.post_add_user_asset_list_queries_by_list(
                model_user.userID, model_queries.result[0]
            )
            self.api_adm_users.get_user_asset_list_queries_by_id(model_user.userID)
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_es_asset_list_queries.delete_saved_query_by_id_remove(model_queries.result[0])

    @allure.title('Test get this user asset list queries.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26071")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26071)
    def test_get_user_asset_list_queries_this(self, bearer_token):
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        tenant_id = self.api_adm_tenants.get_data_current_tenant()
        model_user = self.api_adm_users.post_add_user_customer()
        model_queries = self.api_es_asset_list_queries.post_add_asset_list_queries_only_asset_type(
            bearer_token, asset_type_id, tenant_id.uriName
        )
        try:
            self.api_adm_user_asset_list_queries.post_add_user_asset_list_queries_by_list(
                model_user.userID, model_queries.result[0]
            )
            self.api_adm_users.get_user_asset_list_queries_this(bearer_token)
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_es_asset_list_queries.delete_saved_query_by_id_remove(model_queries.result[0])

    @allure.title('Test get list users short info.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26074")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26074)
    def test_get_list_users_short(self):
        self.api_adm_users.get_list_users_short()

    @allure.title('Test head users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26075")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26075)
    def test_head_users(self):
        self.api_adm_users.head_users()

    @allure.title('Test get users relevance.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26161")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26161)
    def test_get_users_relevance(self):
        self.api_adm_users.get_users_relevance()

    @allure.title('Test get users profile.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26162")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26162)
    def test_get_users_profile(self, bearer_token):
        self.api_adm_users.get_users_profile(bearer_token)

    @allure.title('Test add user customer by integration.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26164")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26164)
    def test_post_add_by_integration_user_customer(self):
        model_user = self.api_adm_users.post_add_by_integration_user_customer()
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test add user stuff by integration.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26163")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26163)
    def test_post_add_by_integration_user_stuff(self):
        model_user = self.api_adm_users.post_add_by_integration_user_staff()
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test change user to stuff.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26166")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26166)
    def test_post_change_to_stuff_users(self):
        model_user = self.api_adm_users.post_add_user_customer()
        self.api_adm_users.post_change_to_stuff_users(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test change user to customer.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26165")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26165)
    def test_post_change_to_customer_users(self):
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.post_change_to_customer_users(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test restore user by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26167")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26167)
    def test_put_restore_user_by_id(self):
        model_user = self.api_adm_users.post_add_user_customer()
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_adm_users.put_restore_user_by_id(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test restore user by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26168")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26168)
    def test_put_restore_user_by_list(self):
        model_user = self.api_adm_users.post_add_user_customer()
        model_user2 = self.api_adm_users.post_add_user_staff()
        model_user3 = self.api_adm_users.post_add_user_customer()
        self.api_adm_users.delete_users_by_list(
            model_user.userID,
            model_user2.userID,
            model_user3.userID
        )
        self.api_adm_users.put_restore_users_by_list(
            model_user.userID,
            model_user2.userID,
            model_user3.userID
        )
        self.api_adm_users.delete_users_by_list(
            model_user.userID,
            model_user2.userID,
            model_user3.userID
        )

    @allure.title('Test get list user districts by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26079")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26079)
    def test_get_user_districts_by_id(self):
        model_user = self.api_adm_users.post_add_user_customer()
        model_districts = self.api_es_districts.post_add_three_districts()
        self.api_adm_user_districts.post_add_three_districts_to_user(model_user.userID, model_districts)
        self.api_adm_users.get_user_districts_by_id(model_user.userID)
        self.api_adm_users.delete_users_by_list(model_user.userID)
        self.api_es_districts.delete_districts_by_list(
            model_districts.districts[0],
            model_districts.districts[1],
            model_districts.districts[2]
        )

    # @allure.title('Test resend the invitation to the user.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26080")
    # @pytest.mark.regress
    # @pytest.mark.test_case_id(26080)
    # @pytest.mark.skip(reason="Отправка повторно письма и смс.")
    # def test_put_user_resend_invitation(self):
    #     model_user = self.api_adm_tenants.get_data_current_tenant()
    #     self.api_adm_users.put_user_resend_invitation(model_user.owner.userID)

    @allure.title('Test get user permissions ui.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26081")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26081)
    def test_get_user_permission_ui_this(self):
        self.api_adm_users.get_user_permission_ui_this()

    @allure.title('Test get user permissions ext.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26082")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26082)
    def test_get_user_permission_ext_this(self):
        self.api_adm_users.get_user_permission_ext_this()

    @allure.title('Test get user profile by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26083")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26083)
    def test_get_user_profile_by_user_id(self):
        model_user = self.api_adm_tenants.get_data_current_tenant()
        self.api_adm_users.get_user_profile_by_user_id(model_user.owner.userID)

    @allure.title('Test get user profile by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26084")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26084)
    def test_get_user_profile_this(self):
        self.api_adm_users.get_user_profile_this()

    @allure.title('Test upload user avatar to server by user ID, data from form.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26090")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26090)
    def test_put_upload_user_avatar_to_server_by_user_id_data_from_form(self):
        model_user = self.api_adm_tenants.get_data_current_tenant()
        model_attach = self.api_adm_users.put_upload_user_avatar_to_server_by_user_id_data_from_form(
            model_user.owner.userID
        )
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)

    @allure.title('Test upload user avatar to server by user ID, data from body.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26094")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26094)
    def test_put_upload_user_avatar_by_user_id_data_from_body(self):
        model_user = self.api_adm_tenants.get_data_current_tenant()
        model_attach = self.api_adm_users.put_upload_user_avatar_by_user_id_data_from_body(
            model_user.owner.userID
        )
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)

    @allure.title('Test upload this user avatar to server, data from body.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26095")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26095)
    def test_put_upload_this_user_avatar_data_from_body(self, bearer_token):
        model_attach = self.api_adm_users.put_upload_this_user_avatar_data_from_body(bearer_token)
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)

    @allure.title('Test upload this user avatar to server, data from form.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26092")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26092)
    def test_put_upload_this_user_avatar_to_server_data_from_form(self, bearer_token):
        model_attach = self.api_adm_users.put_upload_this_user_avatar_to_server_data_from_form(bearer_token)
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)

    @allure.title('Test delete user avatar by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26091")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26091)
    def test_delete_user_avatar_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attach = self.api_adm_users.put_upload_user_avatar_by_user_id_data_from_body(
            model_user.userID
        )
        self.api_adm_users.delete_user_avatar_by_user_id(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)

    @allure.title('Test delete this user avatar.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26100")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26100)
    def test_delete_this_user_avatar(self, bearer_token):
        model_attach = self.api_adm_users.put_upload_this_user_avatar_to_server_data_from_form(bearer_token)
        self.api_adm_users.delete_this_user_avatar(bearer_token)
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)

    @allure.title('Test delete users avatar by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26101")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26101)
    def test_delete_users_avatar_by_list(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_user2 = self.api_adm_users.post_add_user_staff()
        model_user3 = self.api_adm_users.post_add_user_staff()
        model_attach = self.api_adm_users.put_upload_user_avatar_by_user_id_data_from_body(model_user.userID)
        model_attach2 = self.api_adm_users.put_upload_user_avatar_by_user_id_data_from_body(model_user2.userID)
        model_attach3 = self.api_adm_users.put_upload_user_avatar_by_user_id_data_from_body(model_user3.userID)
        self.api_adm_users.delete_users_avatar_by_list(
            model_user.userID,
            model_user2.userID,
            model_user3.userID,
        )
        self.api_adm_users.delete_users_by_list(
            model_user.userID,
            model_user2.userID,
            model_user3.userID,
        )
        self.api_common_attachments.delete_attachments_by_list(
            model_attach.attachmentID,
            model_attach2.attachmentID,
            model_attach3.attachmentID,
        )

    @allure.title('Test get user ratings.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26107")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26107)
    def test_get_user_ratings_by_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_task = self.api_work_tasks.post_add_empty_task(task_type_id[0])
        self.api_work_task_assignment_history.post_add_new_task_to_user(model_user.userID, model_task.id)
        self.api_work_task_ratings.post_task_ratings(model_task.id)
        self.api_adm_users.get_user_ratings_by_id(model_user.userID)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test allows any user to register by invitation ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26109")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26109)
    def test_post_add_users_registration(self):
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_invitation = self.api_adm_invitations.post_add_invitation(model_template.results[0])
        model_user = self.api_adm_users.post_add_users_registration(model_invitation.results[0].id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_adm_invitations.delete_invitations_by_list(model_invitation.results[0].id)
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test verify any user to register.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26110")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26110)
    def test_post_add_users_registration_verify(self):
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_invitation = self.api_adm_invitations.post_add_invitation(model_template.results[0])
        model_user = self.api_adm_users.post_add_users_registration(model_invitation.results[0].id)
        self.api_adm_users.post_add_users_registration_verify(model_user.accountID)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_adm_invitations.delete_invitations_by_list(model_invitation.results[0].id)
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test add anonymous user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26112")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26112)
    def test_post_add_anonymous_user(self):
        model_user = self.api_adm_users.post_add_anonymous_user()
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test get users skills by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26140")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26140)
    def test_get_user_skills_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_skills = self.api_pa_skills.post_add_skills_to_tenant()
        self.api_pa_user_skills.post_add_skills_to_user(
            model_user.userID,
            model_skills.skills[0].skillID
        )
        self.api_adm_users.get_user_skills_by_user_id(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_pa_skills.delete_skill_by_id(model_skills.skills[0].skillID)

    @allure.title('Test get users tags by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26141")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26141)
    def test_get_user_tags_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_adm_user_tags.post_add_tags_to_user(model_user.userID)
        self.api_adm_users.get_user_tags_by_user_id(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test get a list task queries to the this user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26154")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26154)
    def test_get_list_task_queries_to_this_user(self):
        model_district = self.api_es_districts.get_list_districts()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        model_query = self.api_work_task_list_queries.post_task_list_queries(
            model_district.result[0].id,
            work_type_id
        )
        self.api_adm_users.get_list_task_queries_to_this_user()
        self.api_work_task_list_queries.delete_task_list_queries_by_list(model_query.result[0])

    @allure.title('Test get a list task queries to the user by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26153")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26153)
    def test_get_list_task_queries_to_user_by_id(self, bearer_token):
        model_user = self.api_adm_tenants.get_data_current_tenant()
        model_district = self.api_es_districts.get_list_districts()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        model_query = self.api_work_task_list_queries.post_task_list_queries_by_owner_user(
            model_district.result[0].id,
            work_type_id,
            bearer_token
        )
        self.api_adm_users.get_list_task_queries_to_user_by_id(model_user.owner.userID)
        self.api_work_task_list_queries.delete_task_list_queries_by_list_by_owner_user(
            bearer_token,
            model_query.result[0]
        )

    @allure.title('Test get user notifications by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26155")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26155)
    def test_get_user_notifications_by_id(self):
        model_user = self.api_adm_tenants.get_data_current_tenant()
        self.api_adm_users.get_user_notifications_by_id(model_user.owner.userID)

    @allure.title('Test get a list notifications to the current user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26156")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26156)
    def test_get_list_notifications_to_current_user(self):
        self.api_adm_users.get_list_notifications_to_current_user()

    @allure.title('Test get a list users warehouses (deprecated).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26180")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26180)
    def test_get_list_users_warehouses_by_id(self):
        model_owner_user = self.api_adm_tenants.get_data_current_tenant()
        model_warehouses = self.api_wh_warehouses.post_add_warehouses()
        self.api_adm_user_warehouses.post_add_warehouses_to_user(
            model_owner_user.owner.userID,
            model_warehouses[0].result[0]
        )
        self.api_adm_users.get_list_users_warehouses_by_id(model_owner_user.owner.userID)
        self.api_wh_warehouses.delete_warehouse_by_id(model_warehouses[0].result[0])

    @allure.title('Test get list users attributes.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26827")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26827)
    def test_get_list_users_attributes(self):
        self.api_adm_users.get_list_users_attributes()

    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26828")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26828)
    @pytest.mark.parametrize('attribute_type_id, attribute_value', Params.params_user_attributes_body.value)
    def test_post_add_different_attributes_to_user(self, attribute_type_id, attribute_value, request):
        allure.dynamic.title(f"{request.node.callspec.id}")
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_different_attributes_for_stuff_and_customer(attribute_type_id)
        try:
            if attribute_type_id in [6, 7]:
                self.api_common_attribute_list_of_values.post_add_attribute_list_of_value_with_five_fields(model_attribute.values[0])
                self.api_adm_users.post_add_attribute_to_user(
                    model_user.userID,
                    model_attribute.values[0],
                    attribute_value
                    )
            else:
                self.api_adm_users.post_add_attribute_to_user(
                    model_user.userID,
                    model_attribute.values[0],
                    attribute_value
                )
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test add attribute to stuff.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27566")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27566)
    def test_post_add_attribute_to_stuff(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_adm_users.post_add_attribute_to_user(
            model_user.userID,
            model_attribute.values[0],
            "string"
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test add attribute to customer.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27565")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27565)
    def test_post_add_attribute_to_customer(self):
        model_user = self.api_adm_users.post_add_user_customer()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_customer()
        self.api_adm_users.post_add_attribute_to_user(
            model_user.userID,
            model_attribute.values[0],
            "string"
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test add attribute (IsRelevantForTechnician=false, IsRelevantForCustomer=false) to customer.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27568")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27568)
    def test_post_add_attribute_technician_false_customer_false_to_customer(self):
        model_user = self.api_adm_users.post_add_user_customer()
        model_attribute = self.api_common_attributes.post_add_attribute_stuff_and_customer_false()
        self.api_adm_users.post_add_attribute_technician_false_customer_false_to_user(
            model_user.userID,
            model_attribute.values[0]
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test add attribute (IsRelevantForTechnician=false, IsRelevantForCustomer=false) to stuff.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27572")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27572)
    def test_post_add_attribute_technician_false_customer_false_to_stuff(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_stuff_and_customer_false()
        self.api_adm_users.post_add_attribute_technician_false_customer_false_to_user(
            model_user.userID,
            model_attribute.values[0]
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test add deleted attribute to user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27567")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27567)
    def test_post_add_deleted_attribute_to_user(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_different_attributes_for_stuff_and_customer(1)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])
        self.api_adm_users.post_add_deleted_attribute_to_user(
            model_user.userID,
            model_attribute.values[0]
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test add attribute to deleted user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27571")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27571)
    def test_post_add_attribute_to_deleted_user(self):
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.delete_user_by_id(model_user.userID)
        model_attribute = self.api_common_attributes.post_add_different_attributes_for_stuff_and_customer(1)
        self.api_adm_users.post_add_attribute_to_deleted_user(
            model_user.userID,
            model_attribute.values[0]
        )
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test add attribute with empty body to user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27569")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27569)
    def test_post_add_empty_body_to_user(self):
        self.api_adm_users.post_add_empty_body_to_user()

    @allure.title('Test add already added attribute to user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27570")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27570)
    def test_post_add_already_added_attribute_to_user(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_different_attributes_for_stuff_and_customer(1)
        self.api_adm_users.post_add_attribute_to_user(
            model_user.userID,
            model_attribute.values[0],
            "string"
        )
        self.api_adm_users.post_add_already_added_attribute_to_user(
            model_user.userID,
            model_attribute.values[0]
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test add two attributes to user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27589")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27589)
    def test_post_add_two_attributes_to_user(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_different_attributes_for_stuff_and_customer(1)
        model_attribute2 = self.api_common_attributes.post_add_different_attributes_for_stuff_and_customer(1)
        self.api_adm_users.post_add_two_attributes_to_user(
            model_user.userID,
            model_attribute.values[0],
            model_attribute2.values[0],
            "string"
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute2.values[0])

    @allure.title('Test add two attributes to two users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27590")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27590)
    def test_post_add_two_attributes_to_two_users(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_user2 = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_different_attributes_for_stuff_and_customer(1)
        model_attribute2 = self.api_common_attributes.post_add_different_attributes_for_stuff_and_customer(1)
        self.api_adm_users.post_add_two_attributes_to_two_users(
            model_user.userID,
            model_user2.userID,
            model_attribute.values[0],
            model_attribute2.values[0],
            "string"
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user2.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute2.values[0])

    @allure.title('Test get list users attributes, IsRelevantForTechnician=true.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27593")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27593)
    def test_get_list_users_attributes_technician_true(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_adm_users.get_list_users_attributes_technician_true()
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test get list users attributes, IsRelevantForTechnician=false.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27594")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27594)
    def test_get_list_users_attributes_technician_false(self):
        model_user = self.api_adm_users.post_add_user_customer()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_customer()
        self.api_adm_users.get_list_users_attributes_technician_false()
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test get list users attributes, IsRelevantForCustomer=true.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27591")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27591)
    def test_get_list_users_attributes_customer_true(self):
        model_user = self.api_adm_users.post_add_user_customer()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_customer()
        self.api_adm_users.get_list_users_attributes_customer_true()
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test get list users attributes, IsRelevantForCustomer=false.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27592")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27592)
    def test_get_list_users_attributes_customer_false(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_adm_users.get_list_users_attributes_customer_false()
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test get list users attributes by attributeID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27595")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27595)
    def test_get_list_users_attributes_by_attribute_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_adm_users.get_list_users_attributes_by_attribute_id(model_attribute.values[0])
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test get list users attributes by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27596")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27596)
    def test_get_list_users_attributes_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_adm_users.get_list_users_attributes_by_user_id(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test update customer attributes.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27597")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27597)
    def test_put_update_customer_attribute(self):
        model_user = self.api_adm_users.post_add_user_customer()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_customer()
        self.api_adm_users.post_add_attribute_to_user(model_user.userID, model_attribute.values[0], "sting")
        self.api_adm_users.put_update_user_attribute(model_user.userID, model_attribute.values[0])
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test update technician attributes.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27598")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27598)
    def test_put_update_technician_attribute(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_adm_users.post_add_attribute_to_user(model_user.userID, model_attribute.values[0], "sting")
        self.api_adm_users.put_update_user_attribute(model_user.userID, model_attribute.values[0])
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test update user attribute with non existent attribute.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27599")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27599)
    def test_put_update_user_attribute_with_non_existent_attribute(self):
        model_user = self.api_adm_users.post_add_user_staff()
        non_existent_attribute_id = self.api_common_attributes.get_list_attributes_return_non_existent_attribute_id()
        try:
            self.api_adm_users.put_update_user_attribute_with_non_existent_attribute(model_user.userID, non_existent_attribute_id)
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test update user attribute with empty body.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27600")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27600)
    def test_put_update_user_attribute_with_empty_body(self):
        self.api_adm_users.put_update_user_attribute_with_empty_body()

    @allure.title('Test update technician attribute send empty value field.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27601")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27601)
    def test_put_update_user_attribute_with_empty_value_field(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        try:
            self.api_adm_users.put_update_user_attribute_with_empty_value_field(model_user.userID, model_attribute.values[0])
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27602")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27602)
    @pytest.mark.parametrize('attribute_type_id, attribute_value, new_attribute_value', Params.params_update_user_attributes_body.value)
    def test_put_update_different_users_attributes(self, attribute_type_id, attribute_value, new_attribute_value, request):
        allure.dynamic.title(f"{request.node.callspec.id}")
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_different_attributes_for_stuff_and_customer(attribute_type_id)
        try:
            if attribute_type_id in [6, 7]:
                self.api_common_attribute_list_of_values.post_add_attribute_list_of_value_with_five_fields(model_attribute.values[0])
                self.api_adm_users.post_add_attribute_to_user(
                    model_user.userID,
                    model_attribute.values[0],
                    attribute_value
                    )
                self.api_adm_users.put_update_user_attributes(model_user.userID, model_attribute.values[0], new_attribute_value)
                
            else:
                self.api_adm_users.post_add_attribute_to_user(
                    model_user.userID,
                    model_attribute.values[0],
                    attribute_value
                )
                self.api_adm_users.put_update_user_attributes(model_user.userID, model_attribute.values[0], new_attribute_value)
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test update deleted user attribute.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27605")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27605)
    def test_put_update_deleted_user_attribute(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_adm_users.post_add_attribute_to_user(model_user.userID, model_attribute.values[0], "sting")
        self.api_adm_users.delete_user_by_id(model_user.userID)
        try:
            self.api_adm_users.put_update_deleted_user_attribute(model_user.userID, model_attribute.values[0])
        finally:
            self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test delete attribute from user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27622")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27622)
    def test_delete_attribute_from_user(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_adm_users.post_add_attribute_to_user(model_user.userID, model_attribute.values[0], "sting")
        try:
            self.api_adm_users.delete_attribute_from_user(model_user.userID, model_attribute.values[0])
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test delete attribute from two users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27679")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27679)
    def test_delete_attribute_from_two_users(self):
        model_technician = self.api_adm_users.post_add_user_staff()
        model_customer = self.api_adm_users.post_add_user_customer()
        model_attribute_first = self.api_common_attributes.post_add_string_attribute_for_stuff_and_customer()
        model_attribute_second = self.api_common_attributes.post_add_string_attribute_for_stuff_and_customer()
        self.api_adm_users.post_add_two_attributes_to_two_users(
            model_technician.userID,
            model_customer.userID,
            model_attribute_first.values[0],
            model_attribute_second.values[0],
            "sting"
            )
        try:
            self.api_adm_users.delete_two_attributes_from_two_user(
                model_technician.userID,
                model_customer.userID,
                model_attribute_first.values[0],
                model_attribute_second.values[0]
                )
        finally:
            self.api_adm_users.delete_users_by_list(model_technician.userID, model_customer.userID)
            self.api_common_attributes.delete_attributes_by_list(model_attribute_first.values[0], model_attribute_second.values[0])

    @allure.title('Test delete attribute from user with empty body.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27623")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27623)
    def test_delete_attribute_from_user_with_empty_body(self):
        self.api_adm_users.delete_attribute_from_user_with_empty_body()

    @allure.title('Test delete non existent attribute from user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27624")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27624)
    def test_delete_non_existent_attribute_from_user(self):
        model_user = self.api_adm_users.post_add_user_staff()
        non_existent_attribute_id = self.api_common_attributes.get_list_attributes_return_non_existent_attribute_id()
        self.api_adm_users.delete_non_existent_attribute_from_user(model_user.userID, non_existent_attribute_id)
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test delete attribute from non existent user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27625")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27625)
    def test_delete_attribute_from_non_existent_user(self):
        non_existent_user_id = self.api_adm_users.get_non_existent_user_id()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_adm_users.delete_attribute_from_non_existent_user(non_existent_user_id, model_attribute.values[0])
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27632")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27632)
    @pytest.mark.parametrize('attribute_type_id, attribute_value', Params.params_user_attributes_by_id_body.value)
    def test_post_add_different_attributes_to_user_by_user_id(self, attribute_type_id, attribute_value, request):
        allure.dynamic.title(f"{request.node.callspec.id}")
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_different_attributes_for_stuff_and_customer(attribute_type_id)
        try:
            if attribute_type_id in [6, 7]:
                self.api_common_attribute_list_of_values.post_add_attribute_list_of_value_with_five_fields(model_attribute.values[0])
                self.api_adm_users.post_add_attribute_to_user_by_user_id(
                    model_user.userID,
                    model_attribute.values[0],
                    attribute_value
                    )
            else:
                self.api_adm_users.post_add_attribute_to_user_by_user_id(
                    model_user.userID,
                    model_attribute.values[0],
                    attribute_value
                )
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test add attribute to stuff by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27633")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27633)
    def test_post_add_attribute_to_stuff_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_adm_users.post_add_attribute_to_user_by_user_id(
            model_user.userID,
            model_attribute.values[0],
            "string"
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test add attribute to customer by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27634")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27634)
    def test_post_add_attribute_to_customer_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_customer()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_customer()
        self.api_adm_users.post_add_attribute_to_user_by_user_id(
            model_user.userID,
            model_attribute.values[0],
            "string"
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test add deleted attribute to user by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27635")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27635)
    def test_post_add_deleted_attribute_to_user_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_different_attributes_for_stuff_and_customer(1)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])
        self.api_adm_users.post_add_deleted_attribute_to_user_by_user_id(
            model_user.userID,
            model_attribute.values[0]
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test add attribute to deleted user by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27640")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27640)
    def test_post_add_attribute_to_deleted_user_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.delete_user_by_id(model_user.userID)
        model_attribute = self.api_common_attributes.post_add_different_attributes_for_stuff_and_customer(1)
        self.api_adm_users.post_add_attribute_to_deleted_user_by_user_id(
            model_user.userID,
            model_attribute.values[0]
        )
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test add attribute with empty body to user by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27638")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27638)
    def test_post_add_attribute_with_empty_body_to_user_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.post_add_attribute_with_empty_body_to_user_by_user_id(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test add already added attribute to user by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27639")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27639)
    def test_post_add_already_added_attribute_to_user_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_different_attributes_for_stuff_and_customer(1)
        self.api_adm_users.post_add_attribute_to_user(
            model_user.userID,
            model_attribute.values[0],
            "string"
        )
        self.api_adm_users.post_add_already_added_attribute_to_user_by_user_id(
            model_user.userID,
            model_attribute.values[0]
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test add attribute (IsRelevantForTechnician=false, IsRelevantForCustomer=false) to customer by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27637")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27637)
    def test_post_add_attribute_technician_false_customer_false_to_customer_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_customer()
        model_attribute = self.api_common_attributes.post_add_attribute_stuff_and_customer_false()
        self.api_adm_users.post_add_attribute_technician_false_customer_false_to_user_by_user_id(
            model_user.userID,
            model_attribute.values[0]
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test add attribute (IsRelevantForTechnician=false, IsRelevantForCustomer=false) to stuff by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27636")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27636)
    def test_post_add_attribute_technician_false_customer_false_to_stuff_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_stuff_and_customer_false()
        self.api_adm_users.post_add_attribute_technician_false_customer_false_to_user_by_user_id(
            model_user.userID,
            model_attribute.values[0]
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test get user attribute by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26831")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26831)
    def test_get_user_attributes_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_customer()
        model_attribute = self.api_common_attributes.post_add_attribute_for_stuff_and_customer()
        self.api_adm_users.post_add_attribute_to_user_by_user_id(
            model_user.userID,
            model_attribute.values[0],
            "string"
        )
        self.api_adm_users.get_user_attributes_by_user_id(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test get user attributes by userID with IsRelevantForTechnician=true.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27663")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27663)
    def test_get_user_attributes_by_user_id_with_IsRelevantForTechnician_true(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_adm_users.post_add_attribute_to_user_by_user_id(
            model_user.userID,
            model_attribute.values[0],
            "string"
        )
        self.api_adm_users.get_user_attributes_by_user_id_with_IsRelevantForTechnician_true(
            model_user.userID, model_attribute.values[0], "string"
            )
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test get user attributes by userID with IsRelevantForTechnician=false.')
    @pytest.mark.skipif(
        os.environ.get('TENANT_ID') not in ['121', '66', '405'],
        reason="Test only for tenants 121, 66, 405"
        )
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27664")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27664)
    def test_get_user_attributes_by_user_id_with_IsRelevantForTechnician_false(self):
        self.api_common_attributes.deleting_attributes_customer_true_technician_false()
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.get_user_attributes_by_user_id_with_IsRelevantForTechnician_false(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test get user attributes by userID with attributeID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27665")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27665)
    def test_get_user_attributes_by_user_id_with_attribute_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_adm_users.post_add_attribute_to_user_by_user_id(
            model_user.userID,
            model_attribute.values[0],
            "string"
        )
        try:
            self.api_adm_users.get_user_attributes_by_user_id_with_attribute_id(model_user.userID, model_attribute.values[0])
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test get user attributes by userID with non existent attributeID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27666")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27666)
    def test_get_user_attributes_by_user_id_with_non_existent_attribute_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        attribute_id = self.api_common_attributes.get_list_attributes_return_non_existent_attribute_id()
        try:
            self.api_adm_users.get_user_attributes_by_user_id_with_non_existent_attribute_id(model_user.userID, attribute_id)
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27685")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27685)
    @pytest.mark.parametrize('attribute_type_id, attribute_value, new_attribute_value', Params.params_update_user_attributes_body.value)
    def test_put_update_different_users_attributes_by_user_id(self, attribute_type_id, attribute_value, new_attribute_value, request):
        allure.dynamic.title(f"{request.node.callspec.id}")
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_different_attributes_for_stuff_and_customer(attribute_type_id)
        try:
            if attribute_type_id in [6, 7]:
                self.api_common_attribute_list_of_values.post_add_attribute_list_of_value_with_five_fields(model_attribute.values[0])
                self.api_adm_users.post_add_attribute_to_user(
                    model_user.userID,
                    model_attribute.values[0],
                    attribute_value
                    )
                self.api_adm_users.put_update_user_attributes_by_user_id(model_user.userID, model_attribute.values[0], new_attribute_value)
            else:
                self.api_adm_users.post_add_attribute_to_user(
                    model_user.userID,
                    model_attribute.values[0],
                    attribute_value
                )
                self.api_adm_users.put_update_user_attributes_by_user_id(model_user.userID, model_attribute.values[0], new_attribute_value)
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test update customer attribute by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27680")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27680)
    def test_put_update_customer_attribute_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_customer()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_customer()
        self.api_adm_users.post_add_attribute_to_user(model_user.userID, model_attribute.values[0], "sting")
        self.api_adm_users.put_update_user_attribute_by_user_id(model_user.userID, model_attribute.values[0])
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test update technician attribute by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27681")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27681)
    def test_put_update_technician_attribute_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_adm_users.post_add_attribute_to_user(model_user.userID, model_attribute.values[0], "sting")
        self.api_adm_users.put_update_user_attribute_by_user_id(model_user.userID, model_attribute.values[0])
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test update user attribute with non existent attribute.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27682")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27682)
    def test_put_update_user_attribute_with_non_existent_attribute_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        non_existent_attribute_id = self.api_common_attributes.get_list_attributes_return_non_existent_attribute_id()
        try:
            self.api_adm_users.put_update_user_attribute_with_non_existent_attribute_by_user_id(model_user.userID, non_existent_attribute_id)
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test update user attribute with empty body by UserID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27683")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27683)
    def test_put_update_user_attribute_with_empty_body_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.put_update_user_attribute_with_empty_body_by_user_id(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test update technician attribute send empty value field by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27684")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27684)
    def test_put_update_user_attribute_with_empty_value_field_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        try:
            self.api_adm_users.put_update_user_attribute_with_empty_value_field_by_user_id(model_user.userID, model_attribute.values[0])
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test update deleted user attribute by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27606")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27606)
    def test_put_update_deleted_user_attribute_user_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_adm_users.post_add_attribute_to_user(model_user.userID, model_attribute.values[0], "sting")
        self.api_adm_users.delete_user_by_id(model_user.userID)
        try:
            self.api_adm_users.put_update_deleted_user_attribute_by_user_id(model_user.userID, model_attribute.values[0])
        finally:
            self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test delete two attributes from user by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26834")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26834)
    def test_delete_two_attribute_from_user_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        model_attribute_second = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_adm_users.post_add_two_attributes_to_user(
            model_user.userID, 
            model_attribute.values[0],
            model_attribute_second.values[0],
            "string"
            )
        try:
            self.api_adm_users.delete_two_attribute_from_user_by_user_id(
                model_user.userID,
                model_attribute.values[0],
                model_attribute_second.values[0]
                )
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_common_attributes.delete_attributes_by_list(model_attribute.values[0], model_attribute_second.values[0])

    @allure.title('Test delete attribute from user with empty body by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27687")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27687)
    def test_delete_attribute_from_user_with_empty_body_by_user_id(self):
        self.api_adm_users.delete_attribute_from_user_with_empty_body_by_user_id()

    @allure.title('Test delete attribute from user with empty list by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27688")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27688)
    def test_delete_attribute_from_user_with_empty_list_by_user_id(self):
        self.api_adm_users.delete_attribute_from_user_with_empty_list_by_user_id()

    @allure.title('Test delete attribute from non existent user by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27689")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27689)
    def test_delete_attribute_from_non_existent_user_by_user_id(self):
        non_existent_user_id = self.api_adm_users.get_non_existent_user_id()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_adm_users.delete_attribute_from_non_existent_user_by_user_id(non_existent_user_id, model_attribute.values[0])
        self.api_common_attributes.delete_method_attribute_by_id(model_attribute.values[0])

    @allure.title('Test delete already deleted attribute from user by userID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27691")
    @pytest.mark.regress
    @pytest.mark.ng
    @pytest.mark.test_case_id(27691)
    def test_delete_already_deleted_attribute_from_user_by_user_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_attribute = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_adm_users.post_add_attribute_to_user(
            model_user.userID, 
            model_attribute.values[0],
            "string"
            )
        try:
            self.api_adm_users.delete_attribute_from_user(
                model_user.userID,
                model_attribute.values[0],
                )
            self.api_adm_users.delete_already_deleted_attribute_from_user_by_user_id(
                model_user.userID,
                model_attribute.values[0],
                )
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_common_attributes.delete_attributes_by_list(model_attribute.values[0])
