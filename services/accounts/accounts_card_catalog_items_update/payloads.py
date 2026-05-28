
class Payloads:
    @staticmethod
    def build_accounts_card_catalog_items_update_payload(*, item_id: int, name: str) -> list[dict]:
        return [{"id": int(item_id), "name": name}]
