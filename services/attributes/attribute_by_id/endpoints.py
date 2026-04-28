from config.config import HOST


class Endpoints:
    get_attribute_by_id_endpoint = f"{HOST}/Attributes/{{attribute_id}}"
