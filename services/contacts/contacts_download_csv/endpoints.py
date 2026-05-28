from config.config import get_host


class Endpoints:
    @property
    def download_contacts_csv_endpoint(self) -> str:
        return f"{get_host()}/accounts/contacts/download"
