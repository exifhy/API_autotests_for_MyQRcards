import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    add_company_endpoint = f'{HOST}/ES/Companies/'
    delete_companies_endpoint = f'{HOST}/ES/Companies/'

    @staticmethod
    def delete_company_by_id_endpoint(company_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}'

    @staticmethod
    def get_company_by_id_endpoint(company_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}'
