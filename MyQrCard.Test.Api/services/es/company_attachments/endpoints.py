from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_bind_attachments_and_company_endpoint = f'{HOST}/ES/CompanyAttachments'
    delete_unbind_attachments_and_company_endpoint = f'{HOST}/ES/CompanyAttachments'
    post_upload_attachments_to_company_data_from_form_endpoint = f'{HOST}/ES/CompanyAttachments/upload/fromForm'
    post_upload_attachments_to_company_data_from_body_endpoint = f'{HOST}/ES/CompanyAttachments/upload/fromBody'
