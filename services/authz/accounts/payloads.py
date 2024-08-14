

class Payloads:

    @staticmethod
    def authorization_payloads(tenant_id: int, member_id: int) -> dict:
        payloads = {
            "tenantID": tenant_id,
            "tenantMemberID": member_id
        }
        return payloads
