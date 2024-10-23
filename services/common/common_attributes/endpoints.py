import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_add_method_attributes_endpoint = f'{HOST}/COMMON/Attributes'
    get_list_attributes_endpoint = f'{HOST}/COMMON/Attributes'
    put_update_attributes_endpoint = f'{HOST}/COMMON/Attributes'
    delete_mass_attributes_endpoint = f'{HOST}/COMMON/Attributes'

    @staticmethod
    def delete_method_attribute_by_id_endpoint(attribute_id: int) -> str:
        return f'{HOST}/COMMON/Attributes/{attribute_id}'

    @staticmethod
    def get_attribute_by_id_endpoint(attribute_id: int) -> str:
        return f'{HOST}/COMMON/Attributes/{attribute_id}'

    @staticmethod
    def get_available_values_for_attribute_endpoint(attribute_id: int) -> str:
        return f'{HOST}/COMMON/Attributes/{attribute_id}/listofvalues'
