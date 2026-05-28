from config.config import HOST


class Endpoints:
    get_accounts_card_whitelists_endpoint = f"{HOST}/accounts/{{account_id}}/cards/{{card_id}}/whitelists"

