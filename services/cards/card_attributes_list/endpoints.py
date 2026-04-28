from config.config import HOST


class Endpoints:
    get_card_attributes_list_endpoint = f"{HOST}/cards/{{card_id}}/attributes/"
