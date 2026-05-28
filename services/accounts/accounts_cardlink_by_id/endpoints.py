from config.config import HOST


class Endpoints:
    get_accounts_cardlink_by_id_endpoint = f"{HOST}/accounts/{{account_id}}/cards/{{card_id}}/links/{{card_link}}"

