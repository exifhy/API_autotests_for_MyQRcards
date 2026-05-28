from config.config import HOST


class Endpoints:
    update_card_endpoint = f"{HOST}/Cards/{{card_id}}"

