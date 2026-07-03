import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmUserDisabledNotifications(BaseTest):

    @allure.title('Test add user disabled notifications.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25987")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25987)
    def test_post_user_disabled_notifications(self):
        model_user = self.api_adm_users.post_add_user_customer()
        model_get_user = self.api_adm_users.get_user_notifications_by_id(model_user.userID)
        self.api_adm_user_disabled_notifications.post_user_disabled_notifications(
            model_user.userID, model_get_user
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
