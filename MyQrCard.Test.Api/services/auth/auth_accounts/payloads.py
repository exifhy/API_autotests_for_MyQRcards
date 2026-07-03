

class Payloads:

    @staticmethod
    def updating_current_accounts_application_data_payload(
            client_id: str,
            push_token: str,
            app_id: int
    ) -> dict:
        payload = {
            "UniqueClientIdentifier": client_id,
            "ClientTypeID": 1,
            "OperatingSystem": "Android O",
            "ApplicationID": app_id,
            "ApplicationVersion": "v.1.0.0",
            "PushToken": push_token
        }
        return payload

    @staticmethod
    def delete_app_and_device_from_account_payload(
            client_id: str,
            app_id: int,
    ) -> dict:
        payload = {
            "UniqueClientIdentifier": client_id,
            "ApplicationID": app_id,
        }
        return payload

    @staticmethod
    def post_accounts_register_payload(**kwargs) -> dict:
        payload = {
            **kwargs
        }
        return payload
