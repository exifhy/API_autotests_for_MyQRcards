

class Payloads:

    @staticmethod
    def authorization_payloads(tenant_id: int, member_id: int) -> dict:
        payloads = {
            "tenantID": tenant_id,
            "tenantMemberID": member_id
        }
        return payloads

    @staticmethod
    def authorisation_api_user_token_payloads(api_user_token: str) -> dict:
        payloads = {
            "serviceToken": api_user_token
        }
        return payloads
