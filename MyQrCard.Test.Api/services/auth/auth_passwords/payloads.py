

class Payloads:

    @staticmethod
    def change_password_payload(**kwargs) -> dict:
        payload = {
            **kwargs
        }
        return payload
