

class Payloads:

    @staticmethod
    def post_user_disabled_notifications_payload(user_id: int, provider_id: int, status: bool) -> dict:
        payload = {
            "userID": user_id,
            "data": [
                {
                    "providerID": provider_id,
                    "isOn": status
                }
            ]
        }
        return payload
