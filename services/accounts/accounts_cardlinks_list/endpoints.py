from config.config import HOST


class Endpoints:
    get_accounts_cardlinks_endpoint = f"{HOST}/accounts/{{account_id}}/cards/links"

