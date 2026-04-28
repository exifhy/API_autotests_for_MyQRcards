
class Payloads:
    @staticmethod
    def build_subscription_invitation_action_payload(*, push_token: str, client_name: str) -> dict:
        return {
            "pushToken": str(push_token),
            "clientName": str(client_name),
        }
