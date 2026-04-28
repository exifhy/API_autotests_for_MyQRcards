from config.config import HOST


class Endpoints:
    card_link_attribute_counter_endpoint = f"{HOST}/cards/{{token}}/cardLink/attributes/click"
