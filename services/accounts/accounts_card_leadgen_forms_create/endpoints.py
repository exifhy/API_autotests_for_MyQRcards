from config.config import HOST


class Endpoints:
    create_accounts_card_leadgen_form_endpoint = f"{HOST}/accounts/{{account_id}}/cards/{{card_id}}/leadgenforms"
