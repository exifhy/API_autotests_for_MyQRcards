from services.authn.accounts.api_accounts import AccountsAPI


class BaseTest:

    def setup_method(self):
        self.api_accounts = AccountsAPI()
