from config.config import HOST


class Endpoints:
    update_company_endpoint = f"{HOST}/Companies/{{company_id}}"

