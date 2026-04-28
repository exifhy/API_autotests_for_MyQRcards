from config.config import HOST


class Endpoints:
    delete_company_by_id_endpoint = f"{HOST}/Companies/{{company_id}}"

