from config.config import HOST


class Endpoints:
    get_card_link_attributes_endpoint = f"{HOST}/cards/{{token}}/cardLink/attributes"
