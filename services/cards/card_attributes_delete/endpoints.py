from config.config import HOST


class Endpoints:
    delete_card_attributes_endpoint = f"{HOST}/cards/{{card_id}}/attributes"
