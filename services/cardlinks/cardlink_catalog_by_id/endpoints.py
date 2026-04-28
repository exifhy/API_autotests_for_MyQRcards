from config.config import HOST


class Endpoints:
    get_cardlink_catalog_by_id_endpoint = f"{HOST}/cardlinks/{{token}}/catalog/{{catalog_id}}"
