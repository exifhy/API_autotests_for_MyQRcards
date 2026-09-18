from config.config import HOST


class Endpoints:
    get_card_attributes_v2_endpoint = f"{HOST}/Cards/{{card_id}}/attributes/V2"
