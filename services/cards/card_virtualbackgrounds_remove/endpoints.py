from config.config import HOST


class Endpoints:
    card_virtualbackgrounds_remove_endpoint = f"{HOST}/cards/{{card_id}}/virtualbackground"
