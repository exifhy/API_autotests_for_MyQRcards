import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_bind_attachments_to_task_endpoint = f'{HOST}/WORK/taskAttachments'
    delete_unbind_attachments_from_task_endpoint = f'{HOST}/WORK/taskAttachments'
    post_upload_attachments_to_task_from_form_endpoint = f'{HOST}/WORK/taskAttachments/upload/fromForm'
    post_upload_attachments_to_task_from_body_endpoint = f'{HOST}/WORK/taskAttachments/upload/fromBody'
