import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    @staticmethod
    def delete_tenant_member_by_id_endpoint(tenant_member_id: int) -> str:
        return f'{HOST}/ADM/TenantMembers/{tenant_member_id}'

