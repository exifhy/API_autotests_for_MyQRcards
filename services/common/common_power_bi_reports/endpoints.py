from config.config import HOST


class Endpoints:

    get_list_power_bi_reports_endpoint = f'{HOST}/COMMON/PowerBIReports'

    @staticmethod
    def get_power_bi_report_by_id_endpoint(report_id: int) -> str:
        return f'{HOST}/COMMON/PowerBIReports/{report_id}'
