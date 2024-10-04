from config.base_test import BaseTest
import allure
import pytest
from src.enums.params_enums import Params


@allure.epic("Administration")
@allure.feature("Authentication and authorization")
class TestAuthAccounts(BaseTest):

    @allure.title('Test account applications with parameters(range).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23393")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23393)
    def test_get_account_applications_with_range(self):
        self.api_auth_accounts.put_updating_current_accounts_application_data()
        model = self.api_auth_accounts.get_account_applications_with_range()
        self.api_auth_accounts.delete_app_and_device_from_your_current_account(
            client_id=model.result[0].client.uniqueClientIdentifier,
            app_id=model.result[0].application.id
        )

    @allure.title('Test account applications without additional parameters.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23377")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23377)
    def test_get_account_applications(self):
        self.api_auth_accounts.put_updating_current_accounts_application_data()
        model = self.api_auth_accounts.get_account_applications()
        self.api_auth_accounts.delete_app_and_device_from_your_current_account(
            client_id=model.result[0].client.uniqueClientIdentifier,
            app_id=model.result[0].application.id
        )

    @allure.title('Test account applications with parameters(offset, fetch).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23395")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23395)
    @pytest.mark.parametrize('offset, fetch', Params.params_auth_accounts.value)
    def test_get_account_applications_with_offset_fetch(self, offset, fetch):
        self.api_auth_accounts.put_updating_current_accounts_application_data()
        self.api_auth_accounts.get_account_applications_with_offset_fetch(
            offset=offset,
            fetch=fetch
        )

    @allure.title('Test account applications with negative parameters(offset, fetch).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23396")
    @pytest.mark.skip(reason='status code 200!')
    @pytest.mark.regress
    @pytest.mark.test_case_id(23396)
    @pytest.mark.parametrize('key, value', Params.params_auth_accounts_negative.value)
    def test_get_account_applications_with_negative_offset_fetch(self, key, value):
        self.api_auth_accounts.put_updating_current_accounts_application_data()
        self.api_auth_accounts.get_account_applications_with_incorrect_values_in_parameters(key, value)

    @allure.title('Test creates an account with email (if not already created).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23401")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23401)
    @pytest.mark.skip(reason="Clarify what he's doing")
    def post_accounts_register(self):
        self.api_auth_accounts.post_accounts_register()

    @allure.title('Test logout.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23400")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23400)
    def test_post_logout_account(self):
        uniq_client_id, app_id = self.api_auth_accounts.put_updating_current_accounts_application_data()
        self.api_auth_accounts.post_logout_account(
            client_id=uniq_client_id,
            app_id=app_id
        )

    @allure.title('Test returns account data by credentials.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23405")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23405)
    def test_get_accounts_by_credentials(self):
        self.api_auth_accounts.get_accounts_by_credentials()

    @allure.title('Test checks if the account is present by the specified credentials.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23406")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23406)
    def test_head_accounts_by_credentials(self):
        self.api_auth_accounts.head_accounts_by_credentials()

    @allure.title('Test get list of notifications from the log.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23407")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23407)
    def test_get_list_notifications_from_log(self):
        self.api_auth_accounts.get_list_notifications_from_log()
