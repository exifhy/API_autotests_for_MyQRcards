import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_org_units_endpoint = f'{HOST}/ES/OrgUnits'
    get_org_units_root_endpoint = f'{HOST}/ES/OrgUnits/root'

    @staticmethod
    def get_org_units_by_id_endpoint(unit_id: int) -> str:
        return f'{HOST}/ES/OrgUnits/{unit_id}/orgunits'
