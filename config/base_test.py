from services.authn.accounts.api_accounts import AuthnAccountsAPI
from services.authz.accounts.api_accounts import AuthzAccountsAPI
from services.es.assets.api_assets import EsAssetsAPI
from services.es.companies.api_companies import EsCompaniesAPI
from services.es.locations.api_locations import EsLocationsAPI
from services.es.assetlocations.api_assetlocations import EsAssetLocationsAPI
from services.es.districts.api_districts import EsDistrictsAPI
from services.es.asset_districts.api_asset_districts import EsAssetDistrictsAPI
from services.es.asset_work_types.api_asset_work_types import EsAssetWorkTypesAPI
from services.work.work_types.api_work_types import WorkWorkTypesAPI
from services.export.assets.api_assets import ExportAssetsAPI
from services.export.users.api_users import ExportUsersAPI
from services.adm.users.api_adm_users import AdmUsersAPI


class BaseTest:

    def setup_method(self):
        self.api_authn_accounts = AuthnAccountsAPI()
        self.api_authz_accounts = AuthzAccountsAPI()
        self.api_es_assets = EsAssetsAPI()
        self.api_es_companies = EsCompaniesAPI()
        self.api_es_locations = EsLocationsAPI()
        self.api_es_assetlocations = EsAssetLocationsAPI()
        self.api_es_districts = EsDistrictsAPI()
        self.api_es_asset_districts = EsAssetDistrictsAPI()
        self.api_es_asset_work_types = EsAssetWorkTypesAPI()
        self.api_work_work_types = WorkWorkTypesAPI()
        self.api_export_assets = ExportAssetsAPI()
        self.api_export_users = ExportUsersAPI()
        self.api_adm_users = AdmUsersAPI()
