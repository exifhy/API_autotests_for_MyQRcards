from config.config import HOST


class Endpoints:
    update_card_v2_endpoint = f"{HOST}/Cards/{{card_id}}/V2"

