class Payloads:
    @staticmethod
    def post_accounts_register_payload(email: str, mobile_phone: str, domain_login: str) -> dict:
        return {
            "email": email,
            "mobilePhone": mobile_phone,
            "domainLogin": domain_login,
        }
