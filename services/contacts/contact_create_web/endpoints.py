from config.config import get_host


class Endpoints:
    @property
    def create_contact_web_endpoint(self) -> str:
        return f"{get_host()}/accounts/contacts/web"
