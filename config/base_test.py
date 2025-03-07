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
from services.work.work_task_assignment_history.api_work_task_assignment_history import WorkTaskAssignmentHistoryAPI
from services.work.work_task_staging_history.api_work_task_staging_history import WorkTaskStagingHistoryAPI
from services.auth.auth_accounts.api_auth_accounts import AuthAccountsAPI
from services.common.common_applications.api_common_applications import CommonApplicationsAPI
from services.auth.auth_passwords.api_auth_passwords import AuthPasswordsAPI
from services.auth.auth_verification_codes.api_auth_verification_codes import AuthVerificationCodesAPI
from services.auth.auth_messages.api_auth_messages import AuthMessagesAPI
from services.authn.authn_passwords.api_authn_passwords import AuthnPasswordsAPI
from services.authz.access_tokens.api_authz_access_tokens import AuthzAccessTokensAPI
from services.authz.refresh_tokens.api_authz_refresh_tokens import AuthzRefreshTokensAPI
from services.authz.service_tokens.api_authz_service_tokens import AuthzServiceTokensAPI
from services.adm.adm_tenant_members.api_adm_tenant_members import AdmTenantMembersAPI
from services.authz.authz_tokens.api_authz_tokens import AuthzTokensAPI
from services.es.company_locations.api_companies_locations import EsCompanyLocationsAPI
from services.sc.sc_contract_attributes.api_sc_contract_attributes import ScContractAttributesAPI
from services.sc.sc_service_contract.api_sc_service_contract import ScServiceContractAPI
from services.es.asset_types.api_es_asset_types import EsAssetTypesAPI
from services.es.asset_classes.api_es_asset_classes import EsAssetClassesAPI
from services.common.common_attributes.api_common_attributes import CommonAttributesAPI
from services.common.common_attribute_list_of_values.api_common_attribute_list_of_values import CommonAttributeListOfValuesAPI
from services.work.work_task_types.api_work_task_types import WorkTaskTypesAPI
from services.sla.sla_criticalities.api_sla_criticalities import SlaCriticalitiesAPI
from services.common.common_contacts.api_common_contacts import CommonContactsAPI
from services.tstg.tstg_task_stages.api_tstg_task_stages import TstgTaskStagesAPI
from services.tstg.tstg_task_stage_links.api_tstg_task_stage_links import TstgTaskStageLinksAPI
from services.es.asset_attachments.api_es_asset_attachments import EsAssetAttachmentsAPI
from services.common.common_attachments.api_common_attachments import CommonAttachmentsAPI
from services.es.es_asset_attributes.api_es_asset_attributes import EsAssetAttributesAPI
from services.es.es_asset_list_queries.api_es_asset_list_queries import EsAssetListQueriesAPI
from services.adm.adm_tenants.api_adm_tenants import AdmTenantsAPI
from services.work.work_checklists.api_work_checklists import WorkChecklistsAPI
from services.work.work_checklist_items.api_work_checklist_items import WorkChecklistItemsAPI
from services.pa.pa_skills.api_pa_skills import PaSkillsAPI
from services.es.es_asset_skills.api_es_asset_skills import EsAssetSkillsAPI
from services.es.es_asset_schemas.api_es_asset_schemas import EsAssetSchemasAPI
from services.es.es_asset_tags.api_es_asset_tags import EsAssetTagsAPI
from services.es.es_asset_templates.api_es_asset_templates import EsAssetTemplatesAPI
from services.es.es_asset_template_attachments.api_es_asset_template_attachments import EsAssetTemplateAttachmentsAPI
from services.es.es_asset_template_attributes.api_es_asset_template_attributes import EsAssetTemplateAttributesAPI
from services.es.es_asset_template_districts.api_es_asset_template_districts import EsAssetTemplateDistrictsAPI
from services.es.es_asset_template_skills.api_es_asset_template_skills import EsAssetTemplateSkillsAPI
from services.es.es_asset_template_work_types.api_es_asset_template_work_types import EsAssetTemplateWorkTypesAPI
from services.es.company_attachments.api_company_attachments import EsCompanyAttachmentsAPI
from services.common.common_banks.api_common_banks import CommonBanksAPI
from services.es.es_company_registration_types.api_es_company_registration_types import EsCompanyRegistrationTypesAPI
from services.es.es_preferred_technicians.api_es_preferred_technicians import EsPreferredTechniciansAPI
from services.es.es_org_units.api_es_org_units import EsOrgUnitsAPI
from services.work.work_request_methods.api_work_request_methods import WorkRequestMethodsAPI
from services.work.work_completed_works.api_work_completed_works import WorkCompletedWorksAPI
from services.work.work_completed_work_attachments.api_work_completed_work_attachments import WorkCompletedWorkAttachmentsAPI
from services.work.work_task_actualities.api_work_task_actualities import WorkTaskActualitiesAPI
from services.work.work_task_attachments.api_work_task_attachments import WorkTaskAttachmentsAPI
from services.work.work_task_attributes.api_work_task_attributes import WorkTaskAttributesAPI
from services.work.work_task_contacts.api_work_task_contacts import WorkTaskContactsAPI
from services.work.work_task_filter.api_work_task_filter import WorkTaskFilterAPI
from services.work.work_task_conversation_deliveries.api_work_task_conversation_deliveries import WorkTaskConversationDeliveriesAPI
from services.work.work_task_conversations.api_work_task_conversations import WorkTaskConversationsAPI
from services.work.work_task_list_queries.api_work_task_list_queries import WorkTaskListQueriesAPI
from services.work.work_task_order_by.api_work_task_order_by import WorkTaskOrderByAPI
from services.work.work_task_materials.api_work_task_materials import WorkTaskMaterialsAPI
from services.work.work_task_ratings.api_work_task_ratings import WorkTaskRatingsAPI
from services.wh.wh_materials.api_wh_materials import WhMaterialsAPI
from services.wh.wh_warehouses.api_wh_warehouses import WhWarehousesAPI
from services.wh.wh_receipts.api_wh_receipts import WhReceiptsAPI
from services.wh.wh_inventories.api_wh_inventories import WhInventoriesAPI
from services.work.work_task_skills.api_work_task_skills import WorkTaskSkillsAPI
from services.work.work_task_tags.api_work_task_tags import WorkTaskTagsAPI
from services.work.work_task_watch_lists.api_work_task_watch_lists import WorkTaskWatchListsAPI


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
        self.api_work_task_assignment_history = WorkTaskAssignmentHistoryAPI()
        self.api_work_task_staging_history = WorkTaskStagingHistoryAPI()
        self.api_auth_accounts = AuthAccountsAPI()
        self.api_common_applications = CommonApplicationsAPI()
        self.api_auth_passwords = AuthPasswordsAPI()
        self.api_auth_verifications_codes = AuthVerificationCodesAPI()
        self.api_auth_messages = AuthMessagesAPI()
        self.api_authn_passwords = AuthnPasswordsAPI()
        self.api_authz_access_tokens = AuthzAccessTokensAPI()
        self.api_authz_refresh_tokens = AuthzRefreshTokensAPI()
        self.api_authz_service_tokens = AuthzServiceTokensAPI()
        self.api_adm_tenant_members = AdmTenantMembersAPI()
        self.api_authz_tokens = AuthzTokensAPI()
        self.api_es_company_locations = EsCompanyLocationsAPI()
        self.api_sc_contract_attributes = ScContractAttributesAPI()
        self.api_sc_service_contract = ScServiceContractAPI()
        self.api_es_asset_types = EsAssetTypesAPI()
        self.api_es_asset_classes = EsAssetClassesAPI()
        self.api_common_attributes = CommonAttributesAPI()
        self.api_common_attribute_list_of_values = CommonAttributeListOfValuesAPI()
        self.api_work_task_types = WorkTaskTypesAPI()
        self.api_sla_criticalities = SlaCriticalitiesAPI()
        self.api_common_contacts = CommonContactsAPI()
        self.api_tstg_task_stages = TstgTaskStagesAPI()
        self.api_tstg_task_stage_links = TstgTaskStageLinksAPI()
        self.api_es_asset_attachments = EsAssetAttachmentsAPI()
        self.api_common_attachments = CommonAttachmentsAPI()
        self.api_es_asset_attributes = EsAssetAttributesAPI()
        self.api_es_asset_list_queries = EsAssetListQueriesAPI()
        self.api_adm_tenants = AdmTenantsAPI()
        self.api_work_checklists = WorkChecklistsAPI()
        self.api_work_checklist_items = WorkChecklistItemsAPI()
        self.api_pa_skills = PaSkillsAPI()
        self.api_es_asset_skills = EsAssetSkillsAPI()
        self.api_es_asset_schemas = EsAssetSchemasAPI()
        self.api_es_asset_tags = EsAssetTagsAPI()
        self.api_es_asset_templates = EsAssetTemplatesAPI()
        self.api_es_asset_template_attachments = EsAssetTemplateAttachmentsAPI()
        self.api_es_asset_template_attributes = EsAssetTemplateAttributesAPI()
        self.api_es_asset_template_districts = EsAssetTemplateDistrictsAPI()
        self.api_es_asset_template_skills = EsAssetTemplateSkillsAPI()
        self.api_es_asset_template_work_types = EsAssetTemplateWorkTypesAPI()
        self.api_es_company_attachments = EsCompanyAttachmentsAPI()
        self.api_common_banks = CommonBanksAPI()
        self.api_es_company_registration_types = EsCompanyRegistrationTypesAPI()
        self.api_es_preferred_technicians = EsPreferredTechniciansAPI()
        self.api_es_org_units = EsOrgUnitsAPI()
        self.api_work_request_methods = WorkRequestMethodsAPI()
        self.api_work_completed_works = WorkCompletedWorksAPI()
        self.api_work_completed_work_attachments = WorkCompletedWorkAttachmentsAPI()
        self.api_work_task_actualities = WorkTaskActualitiesAPI()
        self.api_work_task_attachments = WorkTaskAttachmentsAPI()
        self.api_work_task_attributes = WorkTaskAttributesAPI()
        self.api_work_task_contacts = WorkTaskContactsAPI()
        self.api_work_task_filter = WorkTaskFilterAPI()
        self.api_work_task_conversation_deliveries = WorkTaskConversationDeliveriesAPI()
        self.api_work_task_conversations = WorkTaskConversationsAPI()
        self.api_work_task_list_queries = WorkTaskListQueriesAPI()
        self.api_work_task_materials = WorkTaskMaterialsAPI()
        self.api_work_task_order_by = WorkTaskOrderByAPI()
        self.api_work_task_ratings = WorkTaskRatingsAPI()
        self.api_wh_materials = WhMaterialsAPI()
        self.api_wh_warehouses = WhWarehousesAPI()
        self.api_wh_receipts = WhReceiptsAPI()
        self.api_wh_inventories = WhInventoriesAPI()
        self.api_work_task_skills = WorkTaskSkillsAPI()
        self.api_work_task_tags = WorkTaskTagsAPI()
        self.api_work_task_watch_lists = WorkTaskWatchListsAPI()
