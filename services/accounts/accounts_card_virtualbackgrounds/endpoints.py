from config.config import HOST


class Endpoints:
    accounts_card_virtualbackgrounds_endpoint = f"{HOST}/accounts/{{account_id}}/cards/{{card_id}}/virtualbackground"
