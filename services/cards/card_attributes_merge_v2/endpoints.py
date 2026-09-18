from config.config import HOST


class Endpoints:
    merge_card_attributes_v2_endpoint = f"{HOST}/Cards/{{card_id}}/attributes/V2"
