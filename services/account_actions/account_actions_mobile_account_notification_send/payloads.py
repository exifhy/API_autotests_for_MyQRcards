
class Payloads:
    @staticmethod
    def build_mobile_account_notification_send_payload(*, push_token: str, guid: str) -> dict:
        return {
            "pushToken": str(push_token),
            "guid": str(guid),
        }
