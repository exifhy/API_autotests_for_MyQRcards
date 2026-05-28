
class Payloads:
    @staticmethod
    def build_accounts_card_whitelists_remove_payload(allowed_account_ids: list[int]) -> list[int]:
        return [int(account_id) for account_id in allowed_account_ids]
