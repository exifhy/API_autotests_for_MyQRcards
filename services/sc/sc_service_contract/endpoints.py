import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_method_for_add_contract_endpoint = f'{HOST}/SC/ServiceContract'
    put_update_method_for_exist_contract_endpoint = f'{HOST}/SC/ServiceContract'
    get_method_list_of_contract_endpoint = f'{HOST}/SC/ServiceContract'
    head_method_total_count_of_contract_endpoint = f'{HOST}/SC/ServiceContract'
    delete_mass_of_contract_endpoint = f'{HOST}/SC/ServiceContract'

    @staticmethod
    def delete_contract_by_id_endpoint(contract_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}'

    @staticmethod
    def post_add_list_object_to_contract_endpoint(contract_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/assets'

    @staticmethod
    def get_list_of_contract_objects_endpoint(contract_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/assets'

    @staticmethod
    def get_method_of_contract_by_id_endpoint(contract_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}'


