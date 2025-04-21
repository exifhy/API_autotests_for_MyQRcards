from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_bind_attachments_to_asset_endpoint = f'{HOST}/ES/AssetAttachments/'
    delete_unbind_attachments_from_asset_endpoint = f'{HOST}/ES/AssetAttachments/'
    post_upload_file_to_asset_endpoint = f'{HOST}/ES/AssetAttachments/upload'
    post_upload_plan_to_asset_data_from_form_endpoint = f'{HOST}/ES/AssetAttachments/upload/fromForm'
    post_upload_attachments_to_asset_data_from_body_endpoint = f'{HOST}/ES/AssetAttachments/upload/fromBody'
