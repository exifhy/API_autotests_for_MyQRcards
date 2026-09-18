from config.config import HOST


class Endpoints:
    get_card_link_attributes_v2_endpoint = f"{HOST}/Cards/{{token}}/cardLink/attributes/V2"
