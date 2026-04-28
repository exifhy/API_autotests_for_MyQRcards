from config.config import HOST


class Endpoints:
    create_accounts_card_v2_endpoint = f"{HOST}/accounts/{{account_id}}/cards/V2"

