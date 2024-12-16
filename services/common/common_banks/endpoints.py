import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_list_banks_endpoint = f'{HOST}/COMMON/Banks'

    @staticmethod
    def get_bank_by_id_endpoint(bank_id: int) -> str:
        return f'{HOST}/COMMON/Banks/{bank_id}'
