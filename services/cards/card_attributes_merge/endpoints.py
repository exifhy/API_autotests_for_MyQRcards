from config.config import HOST


class Endpoints:
    merge_card_attributes_endpoint = f"{HOST}/cards/{{card_id}}/attributes"
