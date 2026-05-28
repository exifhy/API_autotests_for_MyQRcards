from config.config import HOST


class Endpoints:
    patch_accounts_card_v2_endpoint = f"{HOST}/accounts/{{account_id}}/cards/{{card_id}}/V2"

