from services.authn.accounts.api_accounts import AuthnAccountsAPI
from services.authz.accounts.api_accounts import AuthzAccountsAPI
from services.es.assets.api_assets import EsAssetsAPI
from services.es.companies.api_companies import EsCompaniesAPI
from services.es.locations.api_locations import EsLocationsAPI


class BaseTest:

    def setup_method(self):
        self.api_authn_accounts = AuthnAccountsAPI()
        self.api_authz_accounts = AuthzAccountsAPI()
        self.api_es_assets = EsAssetsAPI()
        self.api_es_companies = EsCompaniesAPI()
        self.api_es_locations = EsLocationsAPI()
