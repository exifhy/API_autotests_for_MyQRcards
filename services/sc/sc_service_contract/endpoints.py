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
    def get_method_of_contract_by_id_endpoint(contract_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}'

    @staticmethod
    def post_add_list_object_to_contract_endpoint(contract_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/assets'

    @staticmethod
    def get_list_of_contract_objects_endpoint(contract_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/assets'

    @staticmethod
    def delete_objects_related_to_contracts_endpoint(contract_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/assets'

    @staticmethod
    def delete_objects_related_to_contracts_by_id_endpoint(contract_id: int, asset_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/assets/{asset_id}'

    @staticmethod
    def put_add_object_to_contracts_by_id_endpoint(contract_id: int, asset_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/assets/{asset_id}'

    @staticmethod
    def get_list_attachments_by_contracts_by_id_endpoint(contract_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/attachments'

    @staticmethod
    def post_bind_contract_and_attachment_by_id_endpoint(contract_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/attachments'

    @staticmethod
    def delete_unbind_contract_and_attachment_by_id_endpoint(contract_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/attachments'

    @staticmethod
    def get_attachment_by_contract_by_attachment_id_endpoint(contract_id: int, attachment_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/attachment/{attachment_id}'

    @staticmethod
    def get_temporary_redirect_to_temporary_download_link_endpoint(contract_id: int, attachment_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/attachments/{attachment_id}'

    @staticmethod
    def post_upload_file_to_server_and_bind_contract_data_from_form_endpoint(contract_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/attachments/upload/fromform'

    @staticmethod
    def post_upload_file_to_server_and_bind_contract_data_from_form_v2_endpoint(contract_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/v2/attachments/upload/fromform'

    @staticmethod
    def post_upload_file_to_server_and_bind_contract_data_from_body_endpoint(contract_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/attachments/upload/fromBody'

    @staticmethod
    def get_list_of_user_attributes_by_contract_endpoint(contract_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/attributes'

    @staticmethod
    def get_list_of_contacts_by_contract_endpoint(contract_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/contacts'

    @staticmethod
    def delete_contacts_by_contract_endpoint(contract_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/contacts'

    @staticmethod
    def post_add_contacts_by_contract_endpoint(contract_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/contacts'

    @staticmethod
    def delete_contact_by_contract_by_id_endpoint(contract_id: int, contact_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/contacts/{contact_id}'

    @staticmethod
    def put_contact_to_contract_by_id_endpoint(contract_id: int, contact_id: int) -> str:
        return f'{HOST}/SC/ServiceContract/{contract_id}/contacts/{contact_id}'
