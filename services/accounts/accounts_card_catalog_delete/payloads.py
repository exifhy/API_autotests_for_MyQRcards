
class Payloads:
    @staticmethod
    def build_accounts_card_catalog_delete_payload(catalog_ids: list[int]) -> list[int]:
        return [int(catalog_id) for catalog_id in catalog_ids]
