from config.base_test import BaseTest
import allure
import pytest


@allure.epic("Administration")
@allure.feature("Registration")
class TestAuthzAccounts(BaseTest):

    @allure.title('Test Authorisation of a tenant account.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23038")
    def test_account_authorisation_of_tenant_account(self):
        model = self.api_authn_accounts.account_authentication_by_basic_authorisation()
        self.api_authz_accounts.account_authorisation_of_tenant_account(model.access_token)

    @allure.title('Test Authorisation of a tenant account without tenantMemberID field in the payload.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23039")
    def test_account_authorisation_of_tenant_account_without_member_id_in_body(self):
        model = self.api_authn_accounts.account_authentication_by_basic_authorisation()
        self.api_authz_accounts.account_authorisation_of_tenant_account_without_member_id_in_body(model.access_token)

    @allure.title('Test Authorisation of a tenant account without tenantID field in the payload.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23040")
    def test_account_authorisation_of_tenant_account_without_tenant_id_in_body(self):
        model = self.api_authn_accounts.account_authentication_by_basic_authorisation()
        self.api_authz_accounts.account_authorisation_of_tenant_account_without_tenant_id_in_body(model.access_token)

