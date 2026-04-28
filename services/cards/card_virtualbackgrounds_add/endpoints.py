from config.config import HOST


class Endpoints:
    card_virtualbackgrounds_add_endpoint = f"{HOST}/cards/{{card_id}}/virtualbackground"
