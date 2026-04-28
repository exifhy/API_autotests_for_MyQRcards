from config.config import HOST


class Endpoints:
    get_company_by_id_endpoint = f"{HOST}/Companies/{{company_id}}"

