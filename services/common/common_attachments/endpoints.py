import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_upload_attachments_to_server_endpoint = f'{HOST}/COMMON/Attachments/upload/fromForm'

    @staticmethod
    def delete_attachment_endpoint(attachment_id: int) -> str:
        return f'{HOST}/COMMON/Attachments/{attachment_id}'

