from services.authn.accounts.api_accounts import AuthnAccountsAPI
from services.authz.accounts.api_accounts import AuthzAccountsAPI
from services.es.assets.api_es_assets import EsAssetsAPI
from services.es.companies.api_es_companies import EsCompaniesAPI
from services.es.locations.api_locations import EsLocationsAPI
from services.es.assetlocations.api_assetlocations import EsAssetLocationsAPI
from services.es.districts.api_districts import EsDistrictsAPI
from services.es.asset_districts.api_asset_districts import EsAssetDistrictsAPI
from services.es.asset_work_types.api_asset_work_types import EsAssetWorkTypesAPI
from services.work.work_types.api_work_types import WorkWorkTypesAPI
from services.export.assets.api_export_assets import ExportAssetsAPI
from services.export.users.api_export_users import ExportUsersAPI
from services.adm.users.api_adm_users import AdmUsersAPI
from services.pa.employment.api_employment import PaEmploymentAPI
from services.adm.user_districts.api_user_districts import AdmUserDistrictsAPI
from services.adm.user_roles.api_user_roles import AdmUserRolesAPI
from services.export.companies.api_export_companies import ExportCompaniesAPI
from services.export.materials.api_export_materials import ExportMaterialsAPI
from services.export.material_consumption.api_export_material_consumption import ExportMaterialConsumptionAPI
from services.export.tasks.api_export_tasks import ExportTasksAPI
from services.work.tasks.api_work_tasks import WorkTasksAPI
from services.pmp.schedules.api_pmp_schedules import PmpSchedulesAPI
from services.work.work_task_templates.api_work_task_templates import WorkTaskTemplatesAPI


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
        self.api_pa_employment = PaEmploymentAPI()
        self.api_adm_user_districts = AdmUserDistrictsAPI()
        self.api_adm_user_roles = AdmUserRolesAPI()
        self.api_export_companies = ExportCompaniesAPI()
        self.api_export_materials = ExportMaterialsAPI()
        self.api_export_material_consumption = ExportMaterialConsumptionAPI()
        self.api_export_tasks = ExportTasksAPI()
        self.api_work_tasks = WorkTasksAPI()
        self.api_pmp_schedules = PmpSchedulesAPI()
        self.api_work_task_templates = WorkTaskTemplatesAPI()
