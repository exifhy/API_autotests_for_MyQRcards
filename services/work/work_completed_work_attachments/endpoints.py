import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_completed_work_attachments_endpoint = f'{HOST}/WORK/CompletedWorkAttachments'
    delete_completed_work_attachments_endpoint = f'{HOST}/WORK/CompletedWorkAttachments'
    post_upload_file_to_completed_work_from_form_endpoint = f'{HOST}/WORK/CompletedWorkAttachments/upload/fromForm'
    post_upload_file_to_completed_work_from_body_endpoint = f'{HOST}/WORK/CompletedWorkAttachments/upload/fromBody'
