from config.config import HOST


class Endpoints:
    upload_card_attribute_attachment_endpoint = f"{HOST}/Cards/{{card_id}}/upload/fromForm"
