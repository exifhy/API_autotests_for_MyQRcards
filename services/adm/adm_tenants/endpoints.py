from config.config import HOST


class Endpoints:

    get_data_current_tenant_endpoint = f'{HOST}/ADM/tenants/this'
    get_list_tenants_endpoint = f'{HOST}/ADM/tenants'
    get_list_templates_tenants_endpoint = f'{HOST}/ADM/tenants/templates'
    get_list_feature_flags_tenants_endpoint = f'{HOST}/ADM/tenants/this/featureFlags'
    get_list_licenses_tenant_endpoint = f'{HOST}/ADM/tenants/this/licenses'
    post_add_license_tenant_endpoint = f'{HOST}/ADM/tenants/this/licenses'
    delete_licenses_from_tenant_by_list_endpoint = f'{HOST}/ADM/tenants/this/licenses'

    @staticmethod
    def delete_license_from_tenant_by_id_endpoint(license_id: int) -> str:
        return f'{HOST}/ADM/tenants/this/licenses/{license_id}'

    post_renewal_license_tenant_endpoint = f'{HOST}/ADM/tenants/this/licenses/renewal'
    put_update_license_tenant_endpoint = f'{HOST}/ADM/tenants/licenses'
    get_list_meta_from_tenant_endpoint = f'{HOST}/ADM/tenants/this/meta'
    get_list_packages_from_tenant_endpoint = f'{HOST}/ADM/tenants/this/packages'
    post_add_packages_to_db_cross_tenant_admin_endpoint = f'{HOST}/ADM/tenants/this/packages'
    delete_packages_from_db_cross_tenant_admin_endpoint = f'{HOST}/ADM/tenants/this/packages'
    patch_packages_db_cross_tenant_admin_endpoint = f'{HOST}/ADM/tenants/this/packages'
    post_add_packages_to_tenant_endpoint = f'{HOST}/ADM/tenants/this/packages/tenant'
    delete_packages_from_tenant_endpoint = f'{HOST}/ADM/tenants/this/packages/tenant'
    get_list_variables_from_tenant_endpoint = f'{HOST}/ADM/tenants/this/variables'
    post_add_variables_to_tenant_endpoint = f'{HOST}/ADM/tenants/this/variables'
    put_update_variables_tenant_endpoint = f'{HOST}/ADM/tenants/this/variables'
    delete_variables_from_tenant_by_list_endpoint = f'{HOST}/ADM/tenants/this/variables'

    @staticmethod
    def delete_variables_from_tenant_by_name_endpoint(name: str) -> str:
        return f'{HOST}/ADM/tenants/this/variables/{name}'
