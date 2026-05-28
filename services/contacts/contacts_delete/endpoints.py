from config.config import get_host


class Endpoints:
    @property
    def delete_contacts_endpoint(self) -> str:
        return f"{get_host()}/accounts/contacts"
