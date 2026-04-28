from config.config import HOST


class Endpoints:
    get_card_link_attribute_attachments_endpoint = f"{HOST}/cards/{{token}}/cardLink/attributes/attachments"
