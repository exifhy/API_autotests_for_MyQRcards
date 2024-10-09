import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_add_method_attributes_endpoint = f'{HOST}/COMMON//Attributes'

    @staticmethod
    def delete_method_attribute_endpoint(attribute_id: int) -> str:
        return f'{HOST}/COMMON//Attributes/{attribute_id}'
