import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Service offers application programming interface for warehouses.")
class TestWhUserWarehouses(BaseTest):

    @allure.title('Test get list of user warehouses.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26220")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26220)
    def test_get_list_of_user_warehouses(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_warehouses = self.api_wh_warehouses.post_add_two_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_user_by_user_id(
            model_stuff.userID,
            model_warehouses.result[0],
            model_warehouses.result[1]
        )
        self.api_wh_user_warehouses.get_list_of_user_warehouses(model_stuff.userID)
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        self.api_wh_warehouses.delete_warehouses_by_list(
            model_warehouses.result[0],
            model_warehouses.result[1]
        )

    @allure.title('Test add multiple warehouses to the user, by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26221")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26221)
    @pytest.mark.skip(reason="Тест проходит в - test_delete_multiple_warehouses_from_user_by_user_id.")
    def test_post_add_multiple_warehouses_to_user_by_user_id(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_warehouses = self.api_wh_warehouses.post_add_two_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_user_by_user_id(
            model_stuff.userID,
            model_warehouses.result[0],
            model_warehouses.result[1]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        self.api_wh_warehouses.delete_warehouses_by_list(
            model_warehouses.result[0],
            model_warehouses.result[1]
        )

    @allure.title('Test delete multiple warehouses from user, by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26222")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26222)
    def test_delete_multiple_warehouses_from_user_by_user_id(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_warehouses = self.api_wh_warehouses.post_add_two_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_user_by_user_id(
            model_stuff.userID,
            model_warehouses.result[0],
            model_warehouses.result[1]
        )
        self.api_wh_user_warehouses.delete_multiple_warehouses_from_user_by_user_id(
            model_stuff.userID,
            model_warehouses.result[0],
            model_warehouses.result[1]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        self.api_wh_warehouses.delete_warehouses_by_list(
            model_warehouses.result[0],
            model_warehouses.result[1]
        )

    @allure.title('Test add multiple warehouses to the users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26223")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26223)
    @pytest.mark.skip(reason="Тест проходит в - test_delete_multiple_warehouses_from_users.")
    def test_post_add_multiple_warehouses_to_users(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_stuff2 = self.api_adm_users.post_add_user_staff()
        model_stuff3 = self.api_adm_users.post_add_user_staff()
        model_warehouses = self.api_wh_warehouses.post_add_two_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_users(
            [model_stuff.userID, model_stuff2.userID, model_stuff3.userID],
            [model_warehouses.result[0], model_warehouses.result[1]],
            [model_warehouses.result[0], model_warehouses.result[1]],
            [model_warehouses.result[0], model_warehouses.result[1]]
        )
        self.api_adm_users.delete_users_by_list(
            model_stuff.userID,
            model_stuff2.userID,
            model_stuff3.userID
        )
        self.api_wh_warehouses.delete_warehouses_by_list(
            model_warehouses.result[0],
            model_warehouses.result[1]
        )

    @allure.title('Test add 300 warehouses to the users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_300_warehouses_to_users(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        list_warehouses = self.api_wh_warehouses.post_add_multiple_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_users(
            [model_stuff.userID],
            [list_warehouses]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        self.api_wh_warehouses.delete_list_warehouses(list_warehouses)

    @allure.title('Test add 300 warehouses to 20 users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_300_warehouses_to_20_users(self):
        list_stuff = self.api_adm_users.post_create_multiple_staff_users()
        list_warehouses = self.api_wh_warehouses.post_add_multiple_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_users(
            list_stuff,
            [list_warehouses for _ in range(len(list_stuff))]
        )
        self.api_adm_users.delete_stuff_users_by_list(list_stuff)
        self.api_wh_warehouses.delete_list_warehouses(list_warehouses)

    @allure.title('Test delete 300 warehouses to 20 users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_300_warehouses_from_20_users(self):
        list_stuff = self.api_adm_users.post_create_multiple_staff_users()
        list_warehouses = self.api_wh_warehouses.post_add_multiple_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_users(
            list_stuff,
            [list_warehouses for _ in range(len(list_stuff))]
        )
        self.api_wh_user_warehouses.delete_multiple_warehouses_from_users(
            list_stuff,
            [list_warehouses for _ in range(len(list_stuff))]
        )
        self.api_adm_users.delete_stuff_users_by_list(list_stuff)
        self.api_wh_warehouses.delete_list_warehouses(list_warehouses)

    @allure.title('Test add 300 warehouses to the user, by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_300_warehouses_to_user_by_user_id(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        list_warehouses = self.api_wh_warehouses.post_add_multiple_warehouses()
        self.api_wh_user_warehouses.post_add_list_warehouses_to_user_by_user_id(
            model_stuff.userID,
            list_warehouses
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        self.api_wh_warehouses.delete_list_warehouses(list_warehouses)

    @allure.title('Test delete 300 warehouses from valid user, by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_300_warehouses_from_valid_user(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        list_warehouses = self.api_wh_warehouses.post_add_multiple_warehouses()
        self.api_wh_user_warehouses.post_add_list_warehouses_to_user_by_user_id(
            model_stuff.userID,
            list_warehouses
        )
        self.api_wh_user_warehouses.delete_multiple_warehouses_from_valid_user(
            model_stuff.userID,
            list_warehouses
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        self.api_wh_warehouses.delete_list_warehouses(list_warehouses)

    @allure.title('Test delete multiple warehouses from users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26224")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26224)
    def test_delete_multiple_warehouses_from_users(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_stuff2 = self.api_adm_users.post_add_user_staff()
        model_stuff3 = self.api_adm_users.post_add_user_staff()
        model_warehouses = self.api_wh_warehouses.post_add_two_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_users(
            [model_stuff.userID, model_stuff2.userID, model_stuff3.userID],
            [
                [model_warehouses.result[0], model_warehouses.result[1]],
                [model_warehouses.result[0], model_warehouses.result[1]],
                [model_warehouses.result[0], model_warehouses.result[1]]
            ]
        )
        self.api_wh_user_warehouses.delete_multiple_warehouses_from_users(
            [model_stuff.userID, model_stuff2.userID, model_stuff3.userID],
            [
                [model_warehouses.result[0], model_warehouses.result[1]],
                [model_warehouses.result[0], model_warehouses.result[1]],
                [model_warehouses.result[0], model_warehouses.result[1]]
            ]
        )
        self.api_adm_users.delete_users_by_list(
            model_stuff.userID,
            model_stuff2.userID,
            model_stuff3.userID
        )
        self.api_wh_warehouses.delete_warehouses_by_list(
            model_warehouses.result[0],
            model_warehouses.result[1]
        )

    @allure.title('Test add deleted warehouse to the user, by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_deleted_warehouse_to_user_by_user_id(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_wh_user_warehouses.post_add_deleted_warehouse_to_user_by_user_id(
            model_stuff.userID, model_wh[0].result[0]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)

    @allure.title('Test add warehouse to deleted user, by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_warehouse_to_deleted_user_by_user_id(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_user_warehouses.post_add_warehouse_to_deleted_user_by_user_id(
            model_stuff.userID, model_wh[0].result[0]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add non-existent warehouse to user, by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_non_existent_warehouse_to_user_by_user_id(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        non_existent_wh_id = self.api_wh_warehouses.get_non_existent_warehouse_return_id()
        self.api_wh_user_warehouses.post_add_non_existent_warehouse_to_user_by_user_id(
            model_stuff.userID, non_existent_wh_id
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)

    @allure.title('Test add warehouse to non-existent user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_warehouse_to_non_existent_user(self):
        non_existent_user_id = self.api_adm_users.get_non_existent_user_id()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_user_warehouses.post_add_warehouse_to_non_existent_user(
            non_existent_user_id, model_wh[0].result[0]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add deleted and valid warehouses to valid user, by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_deleted_and_valid_warehouses_to_user(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_two_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh.result[0])
        self.api_wh_user_warehouses.post_add_deleted_and_valid_warehouses_to_user(
            model_stuff.userID, model_wh.result[0], model_wh.result[1]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh.result[1])
        self.api_adm_users.delete_user_by_id(model_stuff.userID)

    @allure.title('Test add deleted and non-existent warehouses to valid user, by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_deleted_and_non_existent_warehouses_to_user(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        non_existent_wh_id = self.api_wh_warehouses.get_non_existent_warehouse_return_id()
        self.api_wh_user_warehouses.post_add_deleted_and_non_existent_warehouses_to_user(
            model_stuff.userID, model_wh[0].result[0], non_existent_wh_id
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)

    @allure.title('Test add already added warehouse to valid user, by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_already_added_warehouse_to_user(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_user_by_user_id(
            model_stuff.userID, model_wh[0].result[0]
        )
        self.api_wh_user_warehouses.post_add_already_added_warehouse_to_user(
            model_stuff.userID, model_wh[0].result[0]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_adm_users.delete_user_by_id(model_stuff.userID)

    @allure.title('Test add unavailable warehouse to user, role without permission <Все склады>.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_unavailable_warehouse_to_user(self, token_power_user_with_tenant_member_id):
        list_app = self.api_common_applications.get_and_return_list_applications()
        model_role = self.api_adm_roles.post_add_role()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_adm_role_applications.post_add_list_role_applications(model_role.results[0], list_app)
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_invitation = self.api_adm_invitations.post_add_invitation(model_template.results[0])
        model_registration = self.api_adm_users.post_add_users_registration(model_invitation.results[0].id)
        self.api_adm_users.post_add_users_registration_verify(model_registration.accountID)
        self.api_adm_users.post_change_to_stuff_users(model_registration.userID)
        self.api_adm_user_roles.post_add_roles_to_user(
            model_registration.userID,
            model_role.results[0]
        )
        tenant_member_id = self.api_adm_tenant_members.get_list_tenant_members_return_tenant_member_id(
            model_registration.userID
        )
        self.api_wh_user_warehouses.post_unavailable_warehouse_to_user(
            token_power_user_with_tenant_member_id(tenant_member_id),
            model_registration.userID,
            model_wh[0].result[0]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_adm_users.delete_user_by_id(model_registration.userID)
        self.api_adm_roles.delete_role_by_id(model_role.results[0])
        self.api_adm_invitations.delete_invitations_by_list(model_invitation.results[0].id)
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test add warehouse to unavailable user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_warehouse_to_unavailable_user(self, token_power_user_with_tenant_member_id):
        list_app = self.api_common_applications.get_and_return_list_applications()
        model_role = self.api_adm_roles.post_add_role()
        self.api_adm_role_applications.post_add_list_role_applications(model_role.results[0], list_app)
        self.api_adm_role_permissions_ext.post_role_permissions_ext(model_role.results[0], 47)
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_invitation = self.api_adm_invitations.post_add_invitation(model_template.results[0])
        model_registration = self.api_adm_users.post_add_users_registration(model_invitation.results[0].id)
        self.api_adm_users.post_add_users_registration_verify(model_registration.accountID)
        self.api_adm_users.post_change_to_stuff_users(model_registration.userID)
        self.api_adm_user_roles.post_add_roles_to_user(
            model_registration.userID,
            model_role.results[0]
        )
        tenant_member_id = self.api_adm_tenant_members.get_list_tenant_members_return_tenant_member_id(
            model_registration.userID
        )
        self.api_wh_user_warehouses.post_warehouse_to_unavailable_user(
            token_power_user_with_tenant_member_id(tenant_member_id),
            model_stuff.userID,
            model_wh[0].result[0]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_adm_users.delete_users_by_list(model_registration.userID, model_stuff.userID)
        self.api_adm_roles.delete_role_by_id(model_role.results[0])
        self.api_adm_invitations.delete_invitations_by_list(model_invitation.results[0].id)
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test add deleted warehouse to the users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_deleted_warehouse_to_users(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_wh_user_warehouses.post_add_deleted_warehouse_to_users(
            [model_stuff.userID], [[model_wh[0].result[0]]]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)

    @allure.title('Test add warehouse to deleted users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_warehouse_to_deleted_users(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_user_warehouses.post_add_warehouse_to_deleted_users(
            [model_stuff.userID], [[model_wh[0].result[0]]]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add non-existent warehouse to users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_non_existent_warehouse_to_users(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        non_existent_wh_id = self.api_wh_warehouses.get_non_existent_warehouse_return_id()
        self.api_wh_user_warehouses.post_add_non_existent_warehouse_to_users(
            [model_stuff.userID], [[non_existent_wh_id]]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)

    @allure.title('Test add warehouse to list non-existent user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_warehouse_to_list_non_existent_user(self):
        non_existent_user_id = self.api_adm_users.get_non_existent_user_id()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_user_warehouses.post_add_warehouse_to_list_non_existent_user(
            [non_existent_user_id], [[model_wh[0].result[0]]]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add valid and non-existent warehouses to list user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_valid_and_non_existent_warehouses_to_list_user(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        non_existent_wh_id = self.api_wh_warehouses.get_non_existent_warehouse_return_id()
        self.api_wh_user_warehouses.post_add_valid_and_non_existent_warehouses_to_list_user(
            [model_stuff.userID], [[model_wh[0].result[0], non_existent_wh_id]]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add valid and deleted warehouses to list user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_valid_and_deleted_warehouses_to_list_user(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_two_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh.result[1])
        self.api_wh_user_warehouses.post_add_valid_and_deleted_warehouses_to_list_user(
            [model_stuff.userID], [[model_wh.result[0], model_wh.result[1]]]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh.result[0])

    @allure.title('Test add deleted and non-existent warehouses to list user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_deleted_and_non_existent_warehouses_to_list_user(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        non_existent_wh_id = self.api_wh_warehouses.get_non_existent_warehouse_return_id()
        self.api_wh_user_warehouses.post_add_deleted_and_non_existent_warehouses_to_list_user(
            [model_stuff.userID], [[model_wh[0].result[0], non_existent_wh_id]]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)

    @allure.title('Test add valid warehouse to valid and deleted users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_valid_warehouse_to_valid_and_deleted_users(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_stuff2 = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_user_warehouses.post_add_valid_warehouse_to_valid_and_deleted_users(
            [model_stuff.userID, model_stuff2.userID], [[model_wh[0].result[0]], [model_wh[0].result[0]]]
        )
        self.api_adm_users.delete_user_by_id(model_stuff2.userID)
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add valid warehouse to valid and deleted users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_valid_warehouse_to_valid_and_non_existent_users(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        non_existent_user_id = self.api_adm_users.get_non_existent_user_id()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_user_warehouses.post_add_valid_warehouse_to_valid_and_non_existent_users(
            [model_stuff.userID, non_existent_user_id], [[model_wh[0].result[0]], [model_wh[0].result[0]]]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add deleted and non-existent warehouses to two valid users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_deleted_and_non_existent_warehouse_to_two_valid_users(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        non_existent_wh_id = self.api_wh_warehouses.get_non_existent_warehouse_return_id()
        self.api_wh_user_warehouses.post_add_deleted_and_non_existent_warehouse_to_two_valid_users(
            [model_stuff.userID, model_stuff.userID], [[model_wh[0].result[0]], [non_existent_wh_id]]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)

    @allure.title('Test add valid, deleted and non-existent warehouses to valid user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_valid_deleted_and_non_existent_warehouse_to_valid_user(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_two_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh.result[0])
        non_existent_wh_id = self.api_wh_warehouses.get_non_existent_warehouse_return_id()
        self.api_wh_user_warehouses.post_add_valid_deleted_and_non_existent_warehouse_to_valid_user(
            [model_stuff.userID], [[model_wh.result[0], non_existent_wh_id, model_wh.result[1]]]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh.result[1])

    @allure.title('Test add already added warehouse to valid user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_already_added_warehouse_to_valid_user(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_users(
            [model_stuff.userID], [[model_wh[0].result[0]]]
        )
        self.api_wh_user_warehouses.post_add_already_added_warehouse_to_valid_user(
            [model_stuff.userID], [[model_wh[0].result[0]]]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add unavailable warehouse to list user, role without permission <Все склады>.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_unavailable_warehouse_to_list_user(self, token_power_user_with_tenant_member_id):
        list_app = self.api_common_applications.get_and_return_list_applications()
        model_role = self.api_adm_roles.post_add_role()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_adm_role_applications.post_add_list_role_applications(model_role.results[0], list_app)
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_invitation = self.api_adm_invitations.post_add_invitation(model_template.results[0])
        model_registration = self.api_adm_users.post_add_users_registration(model_invitation.results[0].id)
        self.api_adm_users.post_add_users_registration_verify(model_registration.accountID)
        self.api_adm_users.post_change_to_stuff_users(model_registration.userID)
        self.api_adm_user_roles.post_add_roles_to_user(
            model_registration.userID,
            model_role.results[0]
        )
        tenant_member_id = self.api_adm_tenant_members.get_list_tenant_members_return_tenant_member_id(
            model_registration.userID
        )
        self.api_wh_user_warehouses.post_add_unavailable_warehouse_to_list_user(
            token_power_user_with_tenant_member_id(tenant_member_id),
            [model_registration.userID],
            [[model_wh[0].result[0]]]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_adm_users.delete_user_by_id(model_registration.userID)
        self.api_adm_roles.delete_role_by_id(model_role.results[0])
        self.api_adm_invitations.delete_invitations_by_list(model_invitation.results[0].id)
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test add warehouse to unavailable list user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_warehouse_to_unavailable_list_user(self, token_power_user_with_tenant_member_id):
        list_app = self.api_common_applications.get_and_return_list_applications()
        model_role = self.api_adm_roles.post_add_role()
        self.api_adm_role_applications.post_add_list_role_applications(model_role.results[0], list_app)
        self.api_adm_role_permissions_ext.post_role_permissions_ext(model_role.results[0], 47)
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_invitation = self.api_adm_invitations.post_add_invitation(model_template.results[0])
        model_registration = self.api_adm_users.post_add_users_registration(model_invitation.results[0].id)
        self.api_adm_users.post_add_users_registration_verify(model_registration.accountID)
        self.api_adm_users.post_change_to_stuff_users(model_registration.userID)
        self.api_adm_user_roles.post_add_roles_to_user(
            model_registration.userID,
            model_role.results[0]
        )
        tenant_member_id = self.api_adm_tenant_members.get_list_tenant_members_return_tenant_member_id(
            model_registration.userID
        )
        self.api_wh_user_warehouses.post_add_warehouse_to_unavailable_list_user(
            token_power_user_with_tenant_member_id(tenant_member_id),
            [model_stuff.userID],
            [[model_wh[0].result[0]]]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_adm_users.delete_users_by_list(model_registration.userID, model_stuff.userID)
        self.api_adm_roles.delete_role_by_id(model_role.results[0])
        self.api_adm_invitations.delete_invitations_by_list(model_invitation.results[0].id)
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test add empty list warehouses to valid user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_empty_list_warehouses_to_owner_user(self):
        self.api_wh_user_warehouses.post_add_empty_list_warehouses_to_owner_user()

    @allure.title('Test add warehouses to users, send empty list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_warehouses_to_user_send_empty_list(self):
        self.api_wh_user_warehouses.post_add_warehouses_to_user_send_empty_list()

    @allure.title('Test delete already deleted warehouse from user, by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_already_deleted_warehouse_from_user_by_user_id(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_user_by_user_id(
            model_stuff.userID, model_wh[0].result[0]
        )
        self.api_wh_user_warehouses.delete_multiple_warehouses_from_user_by_user_id(
            model_stuff.userID, model_wh[0].result[0]
        )
        self.api_wh_user_warehouses.delete_already_deleted_warehouse_from_user_by_user_id(
            model_stuff.userID, model_wh[0].result[0]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_adm_users.delete_user_by_id(model_stuff.userID)

    @allure.title('Test delete deleted from system warehouse from user, by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_deleted_from_system_warehouse_from_user_by_user_id(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_user_by_user_id(
            model_stuff.userID, model_wh[0].result[0]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_wh_user_warehouses.delete_deleted_from_system_warehouse_from_user_by_user_id(
            model_stuff.userID, model_wh[0].result[0]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)

    @allure.title('Test delete warehouse from deleted user, by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_warehouse_from_deleted_user_by_user_id(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_user_by_user_id(
            model_stuff.userID, model_wh[0].result[0]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        self.api_wh_user_warehouses.delete_warehouse_from_deleted_user_by_user_id(
            model_stuff.userID, model_wh[0].result[0]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test delete deleted and valid warehouses from user, by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_deleted_and_valid_warehouses_from_user_by_user_id(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_two_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_user_by_user_id(
            model_stuff.userID, model_wh.result[0], model_wh.result[1]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh.result[0])
        self.api_wh_user_warehouses.delete_deleted_and_valid_warehouses_from_user_by_user_id(
            model_stuff.userID, model_wh.result[0], model_wh.result[1]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh.result[1])

    @allure.title('Test delete valid warehouse from non-existent user, by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_valid_warehouse_from_non_existent_user(self):
        non_existent_user_id = self.api_adm_users.get_non_existent_user_id()
        model_wh = self.api_wh_warehouses.post_add_warehouses()

        self.api_wh_user_warehouses.delete_valid_warehouse_from_non_existent_user(
            non_existent_user_id, model_wh[0].result[0]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test delete non-existent warehouse from non-existent user, by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_non_existent_warehouse_from_non_existent_user(self):
        non_existent_user_id = self.api_adm_users.get_non_existent_user_id()
        non_existent_wh_id = self.api_wh_warehouses.get_non_existent_warehouse_return_id()
        self.api_wh_user_warehouses.delete_non_existent_warehouse_from_non_existent_user(
            non_existent_user_id, non_existent_wh_id
        )

    @allure.title('Test delete non-existent warehouse from valid user, by user ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_non_existent_warehouse_from_valid_user(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        non_existent_wh_id = self.api_wh_warehouses.get_non_existent_warehouse_return_id()
        self.api_wh_user_warehouses.delete_non_existent_warehouse_from_valid_user(
            model_stuff.userID, non_existent_wh_id
        )

    @allure.title('Test delete already deleted warehouse from user.(/UserWarehouses).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_already_deleted_warehouses_from_users_by_body(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_user_by_user_id(
            model_stuff.userID, model_wh[0].result[0]
        )
        self.api_wh_user_warehouses.delete_multiple_warehouses_from_user_by_user_id(
            model_stuff.userID, model_wh[0].result[0]
        )
        self.api_wh_user_warehouses.delete_already_deleted_warehouses_from_users_by_body(
            [model_stuff.userID], [[model_wh[0].result[0]]]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_adm_users.delete_user_by_id(model_stuff.userID)

    @allure.title('Test delete deleted from system warehouse from user.(/UserWarehouses).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_deleted_from_system_warehouses_from_users_by_body(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_user_by_user_id(
            model_stuff.userID, model_wh[0].result[0]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_wh_user_warehouses.delete_deleted_from_system_warehouses_from_users_by_body(
            [model_stuff.userID], [[model_wh[0].result[0]]]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)

    @allure.title('Test delete valid warehouse from deleted user.(/UserWarehouses).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_valid_warehouse_from_deleted_users_by_body(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_user_by_user_id(
            model_stuff.userID, model_wh[0].result[0]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        self.api_wh_user_warehouses.delete_valid_warehouse_from_deleted_users_by_body(
            [model_stuff.userID], [[model_wh[0].result[0]]]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test delete valid and non-existent warehouses from user.(/UserWarehouses).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_valid_and_non_existent_warehouses_from_users_by_body(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        non_existent_wh_id = self.api_wh_warehouses.get_non_existent_warehouse_return_id()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_user_by_user_id(
            model_stuff.userID, model_wh[0].result[0]
        )
        self.api_wh_user_warehouses.delete_valid_and_non_existent_warehouses_from_users_by_body(
            [model_stuff.userID], [[model_wh[0].result[0], non_existent_wh_id]]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_adm_users.delete_user_by_id(model_stuff.userID)

    @allure.title('Test delete already deleted and non-existent warehouses from user.(/UserWarehouses).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_already_deleted_and_non_existent_warehouses_from_users_by_body(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        non_existent_wh_id = self.api_wh_warehouses.get_non_existent_warehouse_return_id()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_user_by_user_id(
            model_stuff.userID, model_wh[0].result[0]
        )
        self.api_wh_user_warehouses.delete_multiple_warehouses_from_user_by_user_id(
            model_stuff.userID, model_wh[0].result[0]
        )
        self.api_wh_user_warehouses.delete_already_deleted_and_non_existent_warehouses_from_users_by_body(
            [model_stuff.userID], [[model_wh[0].result[0], non_existent_wh_id]]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_adm_users.delete_user_by_id(model_stuff.userID)

    @allure.title('Test delete valid warehouses from valid and deleted from system users.(/UserWarehouses).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_valid_warehouses_from_valid_and_deleted_users_by_body(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_stuff2 = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_users(
            [model_stuff.userID, model_stuff2.userID],
            [[model_wh[0].result[0]], [model_wh[0].result[0]]]
        )
        self.api_adm_users.delete_user_by_id(model_stuff2.userID)
        self.api_wh_user_warehouses.delete_valid_warehouses_from_valid_and_deleted_users_by_body(
            [model_stuff.userID, model_stuff2.userID],
            [[model_wh[0].result[0]], [model_wh[0].result[0]]]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_adm_users.delete_user_by_id(model_stuff.userID)

    @allure.title('Test delete valid warehouses from non-existent and deleted from system users.(/UserWarehouses).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_valid_warehouses_from_non_existent_and_deleted_users_by_body(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        non_existent_user_id = self.api_adm_users.get_non_existent_user_id()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_users(
            [model_stuff.userID],
            [[model_wh[0].result[0]]]
        )
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        self.api_wh_user_warehouses.delete_valid_warehouses_from_non_existent_and_deleted_users_by_body(
            [model_stuff.userID, non_existent_user_id],
            [[model_wh[0].result[0]], [model_wh[0].result[0]]]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test get list of unavailable user warehouses.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_of_unavailable_user_warehouses(self, token_power_user_with_tenant_member_id):
        model_stuff = self.api_adm_users.post_add_user_staff()
        list_app = self.api_common_applications.get_and_return_list_applications()
        model_role = self.api_adm_roles.post_add_role()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_adm_role_applications.post_add_list_role_applications(model_role.results[0], list_app)
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_invitation = self.api_adm_invitations.post_add_invitation(model_template.results[0])
        model_registration = self.api_adm_users.post_add_users_registration(model_invitation.results[0].id)
        self.api_adm_users.post_add_users_registration_verify(model_registration.accountID)
        self.api_adm_users.post_change_to_stuff_users(model_registration.userID)
        self.api_adm_user_roles.post_add_roles_to_user(
            model_registration.userID,
            model_role.results[0]
        )
        tenant_member_id = self.api_adm_tenant_members.get_list_tenant_members_return_tenant_member_id(
            model_registration.userID
        )
        self.api_wh_user_warehouses.post_add_multiple_warehouses_to_user_by_user_id(
            model_stuff.userID,
            model_wh[0].result[0]
        )
        self.api_wh_user_warehouses.get_list_of_unavailable_user_warehouses(
            token_power_user_with_tenant_member_id(tenant_member_id),
            model_stuff.userID
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_adm_users.delete_user_by_id(model_registration.userID)
        self.api_adm_roles.delete_role_by_id(model_role.results[0])
        self.api_adm_invitations.delete_invitations_by_list(model_invitation.results[0].id)
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test get list of non-existent user warehouses.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_of_deleted_user_warehouses(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.delete_user_by_id(model_stuff.userID)
        self.api_wh_user_warehouses.get_list_of_deleted_user_warehouses(model_stuff.userID)
