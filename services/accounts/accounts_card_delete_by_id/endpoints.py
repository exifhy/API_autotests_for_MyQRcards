from config.config import HOST


class Endpoints:
    delete_accounts_card_by_id_endpoint = f"{HOST}/accounts/{{account_id}}/cards/{{card_id}}"

