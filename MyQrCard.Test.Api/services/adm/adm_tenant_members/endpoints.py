from config.config import HOST


class Endpoints:

    get_tenant_member_this_endpoint = f'{HOST}/ADM/TenantMembers/this'
    get_list_tenant_members_endpoint = f'{HOST}/ADM/TenantMembers'
    post_add_tenant_members_endpoint = f'{HOST}/ADM/TenantMembers'
    put_update_tenant_members_endpoint = f'{HOST}/ADM/TenantMembers'
    delete_tenant_members_endpoint = f'{HOST}/ADM/TenantMembers'
    get_returns_api_user_in_current_tenant_endpoint = f'{HOST}/ADM/TenantMembers/apiUser'
    get_anonymous_user_this_tenant_endpoint = f'{HOST}/ADM/TenantMembers/anonymousUser'

    @staticmethod
    def delete_tenant_member_by_id_endpoint(tenant_member_id: int) -> str:
        return f'{HOST}/ADM/TenantMembers/{tenant_member_id}'

    @staticmethod
    def get_tenant_member_by_id_endpoint(tenant_member_id: int) -> str:
        return f'{HOST}/ADM/TenantMembers/{tenant_member_id}'

