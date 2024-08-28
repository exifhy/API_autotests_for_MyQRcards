import os


HOST = "https://dev-api.hubex.ru/fsm" if os.environ["ENVIRON"] == 'qa' else "https://api.hubex.ru/fsm"


class Endpoints:

    add_company_endpoint = f'{HOST}/ES/Companies/'
    delete_companies_endpoint = f'{HOST}/ES/Companies/'

    @staticmethod
    def delete_company_by_id_endpoint(company_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}'
