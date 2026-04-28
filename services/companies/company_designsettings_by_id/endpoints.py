from config.config import HOST


class Endpoints:
    get_company_designsettings_endpoint = f"{HOST}/Companies/{{company_id}}/designsettings"

