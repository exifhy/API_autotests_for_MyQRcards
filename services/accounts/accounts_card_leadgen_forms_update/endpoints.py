from config.config import HOST


class Endpoints:
    update_accounts_card_leadgen_forms_endpoint = f"{HOST}/accounts/{{account_id}}/cards/{{card_id}}/leadgenforms"
