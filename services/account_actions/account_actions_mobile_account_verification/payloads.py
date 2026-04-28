
class Payloads:
    @staticmethod
    def build_mobile_account_verification_payload(
        *,
        push_token: str,
        client_name: str,
        is_accept_advertising: bool = False,
    ) -> dict:
        return {
            "pushToken": str(push_token),
            "clientName": str(client_name),
            "IsAcceptAdvertising": is_accept_advertising,
        }
