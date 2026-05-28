from config.config import HOST


class Endpoints:
    delete_attribute_by_id_endpoint = f"{HOST}/Attributes/{{attribute_id}}"
