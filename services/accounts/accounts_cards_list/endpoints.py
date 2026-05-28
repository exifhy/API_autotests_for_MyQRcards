from config.config import HOST


class Endpoints:
    get_accounts_cards_endpoint = f"{HOST}/accounts/{{account_id}}/cards"

