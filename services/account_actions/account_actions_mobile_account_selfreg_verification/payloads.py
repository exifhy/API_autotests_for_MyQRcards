
class Payloads:
    @staticmethod
    def build_mobile_account_selfreg_verification_payload(*, push_token: str, guid: str) -> dict:
        return {
            "pushToken": str(push_token),
            "guid": str(guid),
        }
