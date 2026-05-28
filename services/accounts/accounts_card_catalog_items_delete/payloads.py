
class Payloads:
    @staticmethod
    def build_accounts_card_catalog_items_delete_payload(item_ids: list[int]) -> list[int]:
        return [int(item_id) for item_id in item_ids]
