from config.config import HOST


class Endpoints:

    post_upload_attachments_to_server_endpoint = f'{HOST}/COMMON/Attachments/upload/fromForm'
    post_upload_attachments_to_server_from_form_v2_endpoint = f'{HOST}/COMMON/Attachments/v2/upload/fromForm'
    post_upload_attachments_to_server_from_body_endpoint = f'{HOST}/COMMON/Attachments/upload/fromBody'

    @staticmethod
    def get_attachments_link_endpoint(attach_id: int) -> str:
        return f'{HOST}/COMMON/Attachments/{attach_id}'

    @staticmethod
    def delete_attachment_endpoint(attachment_id: int) -> str:
        return f'{HOST}/COMMON/Attachments/{attachment_id}'

    @staticmethod
    def get_attachment_container_endpoint(container_id: int, file_path: str) -> str:
        return f'{HOST}/COMMON/Attachments/content/{container_id}/{file_path}'

    delete_attachments_by_list_endpoint = f'{HOST}/COMMON/Attachments'
    get_list_attachments_endpoint = f'{HOST}/COMMON/Attachments'

    @staticmethod
    def get_attachment_data_by_id_endpoint(attach_id: int) -> str:
        return f'{HOST}/COMMON/Attachments/{attach_id}/this'

    @staticmethod
    def post_attachment_publish_endpoint(attach_id: int) -> str:
        return f'{HOST}/COMMON/Attachments/{attach_id}/publish'

    @staticmethod
    def post_attachment_unpublish_endpoint(attach_id: int) -> str:
        return f'{HOST}/COMMON/Attachments/{attach_id}/unpublish'

    get_list_download_link_attachments_endpoint = f'{HOST}/COMMON/Attachments/downloadLink'

    @staticmethod
    def get_attachments_roles_endpoint(attach_id: int) -> str:
        return f'{HOST}/COMMON/Attachments/{attach_id}/roles'
