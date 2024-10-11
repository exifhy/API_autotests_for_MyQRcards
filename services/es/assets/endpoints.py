import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_directory_of_objects_available_to_user_endpoint = f'{HOST}/ES/assets'
    create_object_endpoint = f'{HOST}/ES/assets'

    @staticmethod
    def delete_object_by_id_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}'

    @staticmethod
    def detailed_information_on_object_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}'

    @staticmethod
    def method_of_publishing_an_object_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/publish'

    @staticmethod
    def update_object_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}'

