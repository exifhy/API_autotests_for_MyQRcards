

class Payloads:

    @staticmethod
    def api_token_payload(user_id: int) -> list:
        return [user_id]
