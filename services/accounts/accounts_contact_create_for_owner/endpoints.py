from config.config import HOST


class Endpoints:
    create_contact_for_owner_endpoint = f"{HOST}/accounts/{{account_id}}/contacts"
