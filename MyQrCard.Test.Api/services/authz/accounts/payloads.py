

class Payloads:

    @staticmethod
    def authorization_payloads(tenant_id: str, member_id: str) -> dict:
        payloads = {
            "tenantID": int(tenant_id),
            "tenantMemberID": int(member_id)
        }
        return payloads

    @staticmethod
    def authorization_without_tenant_id_payloads(tenant_id: str) -> dict:
        payloads = {
            "tenantMemberID": int(tenant_id)
        }
        return payloads

    @staticmethod
    def authorization_without_tenant_member_id_payloads(tenant_id: str) -> dict:
        payloads = {
            "tenantID": int(tenant_id)
        }
        return payloads

    @staticmethod
    def authorization_api_user_token_payloads(api_user_token: str) -> dict:
        payloads = {
            "serviceToken": api_user_token
        }
        return payloads
