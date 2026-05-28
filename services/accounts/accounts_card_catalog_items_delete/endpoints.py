from config.config import HOST


class Endpoints:
    delete_accounts_card_catalog_items_endpoint = (
        f"{HOST}/accounts/{{account_id}}/cards/{{card_id}}/catalog/{{catalog_id}}"
    )

