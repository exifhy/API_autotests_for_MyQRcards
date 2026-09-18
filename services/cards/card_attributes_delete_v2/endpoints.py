from config.config import HOST


class Endpoints:
    delete_card_attribute_v2_endpoint = f"{HOST}/Cards/{{card_id}}/attributes/V2/{{card_attribute_node_id}}"
