from config.config import HOST


class Endpoints:
    get_card_attribute_attachments_endpoint = f"{HOST}/cards/{{card_id}}/attributes/attachments"
