
class Payloads:
    @staticmethod
    def build_accept_advertising_payload(is_accept_advertising: bool) -> dict:
        return {
            "isAcceptAdvertising": is_accept_advertising,
        }
