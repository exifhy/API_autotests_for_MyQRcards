from services.authn.accounts.api_accounts import AuthnAccountsAPI


class BaseTest:

    def setup_method(self):
        self.api_authn_accounts = AuthnAccountsAPI()
