from config.config import HOST


class Endpoints:
    update_card_indexing_endpoint = f"{HOST}/Cards/{{card_id}}/indexing"
