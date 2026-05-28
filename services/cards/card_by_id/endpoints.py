from config.config import HOST


class Endpoints:
    get_card_by_id_endpoint = f"{HOST}/Cards/{{card_id}}"
