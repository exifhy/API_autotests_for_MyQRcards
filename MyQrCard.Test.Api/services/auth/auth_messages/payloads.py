

class Payloads:

    @staticmethod
    def messages_verify_payloads(account_id: int, **kwargs) -> dict:
        payload = {
            "accountID": account_id,
            **kwargs
        }
        return payload

    @staticmethod
    def request_password_change(value: str) -> dict:
        payload = {
            "credentials": value
        }
        return payload
