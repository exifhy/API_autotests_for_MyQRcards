from config.config import HOST


class Endpoints:
    delete_many_accounts_cards_endpoint = f"{HOST}/accounts/{{account_id}}/cards/bulkremove"

