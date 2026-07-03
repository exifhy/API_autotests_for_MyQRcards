

class Payloads:

    @staticmethod
    def updates_resource_access_token_payload(access_token: str, refresh_token: str) -> dict:
        payload = {
            "refreshJwt": refresh_token,
            "accessJwt": access_token
        }
        return payload
