from config.config import HOST


class Endpoints:
    get_powerbi_report_by_id_endpoint = f"{HOST}/powerbireports/{{report_id}}"
