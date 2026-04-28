from config.config import HOST


class Endpoints:
    get_contact_by_id_endpoint = f"{HOST}/accounts/contacts/{{contact_id}}"
