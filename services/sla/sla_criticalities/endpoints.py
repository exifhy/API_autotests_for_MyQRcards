import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_list_criticalities_endpoint = f'{HOST}/SLA/Criticalities'
    put_update_criticalities_endpoint = f'{HOST}/SLA/Criticalities'
    post_add_new_criticalities_endpoint = f'{HOST}/SLA/Criticalities'
    delete_criticalities_endpoint = f'{HOST}/SLA/Criticalities'

    @staticmethod
    def get_criticality_by_id(criticality_id: int) -> str:
        return f'{HOST}/SLA/Criticalities/{criticality_id}'

    @staticmethod
    def delete_criticality_by_id(criticality_id: int) -> str:
        return f'{HOST}/SLA/Criticalities/{criticality_id}'
