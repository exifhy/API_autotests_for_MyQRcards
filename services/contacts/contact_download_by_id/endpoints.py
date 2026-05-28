from config.config import get_host


class Endpoints:
    @property
    def download_contact_by_id_endpoint(self) -> str:
        return f"{get_host()}/accounts/contacts/{{contact_id}}/download"
