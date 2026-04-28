from config.config import HOST


class Endpoints:
    create_accounts_card_endpoint = f"{HOST}/accounts/{{account_id}}/cards"

