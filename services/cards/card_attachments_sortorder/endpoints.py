from config.config import HOST


class Endpoints:
    card_attachments_sortorder_endpoint = f"{HOST}/Cards/{{card_id}}/attachments/sortorder"
