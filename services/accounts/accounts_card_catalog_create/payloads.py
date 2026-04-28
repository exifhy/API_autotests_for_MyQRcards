
class Payloads:
    @staticmethod
    def build_accounts_card_catalog_create_payload(*, name: str) -> list[dict]:
        return [{"name": name}]
