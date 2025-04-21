from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_returns_api_user_in_current_tenant_endpoint = f'{HOST}/ADM/TenantMembers/apiUser'

    @staticmethod
    def delete_tenant_member_by_id_endpoint(tenant_member_id: int) -> str:
        return f'{HOST}/ADM/TenantMembers/{tenant_member_id}'

