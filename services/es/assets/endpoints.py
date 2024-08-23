import os


HOST = "https://dev-api.hubex.ru/fsm" if os.environ["ENVIRON"] == 'qa' else "https://api.hubex.ru/fsm"


class Endpoints:

    get_directory_of_objects_available_to_user_endpoint = f'{HOST}/ES/assets'
    create_object_endpoint = f'{HOST}/ES/assets'

    @staticmethod
    def marks_object_as_remote_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets{asset_id}'

    @staticmethod
    def detailed_information_on_object_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets{asset_id}'

