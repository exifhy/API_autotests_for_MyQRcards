import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Users management")
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

    @allure.title('Test resend the invitation to the user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26080")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26080)
    @pytest.mark.skip(reason="Отправка повторно письма и смс.")
    def test_put_user_resend_invitation(self):
        model_user = self.api_adm_tenants.get_data_current_tenant()
        self.api_adm_users.put_user_resend_invitation(model_user.owner.userID)

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
