
class Payloads:
    @staticmethod
    def build_client_tokens_merge_payload(*, client_id: str, push_token: str) -> dict:
        return {
            "clientID": str(client_id),
            "pushToken": str(push_token),
        }
