from config.config import HOST


class Endpoints:
    get_accounts_card_catalog_by_id_endpoint = (
        f"{HOST}/accounts/{{account_id}}/cards/{{card_id}}/catalog/{{catalog_id}}"
    )

