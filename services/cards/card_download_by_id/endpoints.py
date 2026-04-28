from config.config import HOST


class Endpoints:
    get_card_download_by_id_endpoint = f"{HOST}/Cards/{{card_id}}/download"
