import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_bind_attachments_to_asset_template_endpoint = f'{HOST}/ES/assetTemplateAttachments'
    delete_attachments_from_asset_template_endpoint = f'{HOST}/ES/assetTemplateAttachments'
    post_upload_attachment_to_template_data_from_form_endpoint = f'{HOST}/ES/assetTemplateAttachments/upload/fromForm'
    post_upload_attachment_to_template_data_from_body_endpoint = f'{HOST}/ES/assetTemplateAttachments/upload/fromBody'

