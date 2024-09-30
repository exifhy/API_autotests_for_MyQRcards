

class Payloads:

    @staticmethod
    def accounts_sms_send_payload(phone: str) -> dict:
        return {"phone": phone}

    @staticmethod
    def accounts_sms_login_payload(code: str, phone: str) -> dict:
        return {
            "code": code,
            "phone": phone
        }
