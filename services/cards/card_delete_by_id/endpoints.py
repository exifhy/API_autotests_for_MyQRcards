from config.config import HOST


class Endpoints:
    delete_card_by_id_endpoint = f"{HOST}/Cards/{{card_id}}"
