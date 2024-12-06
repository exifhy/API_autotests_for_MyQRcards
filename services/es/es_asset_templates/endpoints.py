import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    @staticmethod
    def get_list_attachments_from_asset_template_endpoint(asset_template_id: int) -> str:
        return f'{HOST}/ES/AssetTemplates/{asset_template_id}/attachments'

    @staticmethod
    def get_attachment_from_asset_template_by_id_endpoint(asset_template_id: int, attachment_id: int) -> str:
        return f'{HOST}/ES/AssetTemplates/{asset_template_id}/attachments/{attachment_id}'

    @staticmethod
    def get_list_attributes_asset_template_endpoint(asset_template_id: int) -> str:
        return f'{HOST}/ES/AssetTemplates/{asset_template_id}/attributes'

    @staticmethod
    def put_upload_avatar_to_asset_template_data_from_from_endpoint(asset_template_id: int) -> str:
        return f'{HOST}/ES/AssetTemplates/{asset_template_id}/avatar/upload/fromForm'

    @staticmethod
    def put_upload_avatar_to_asset_template_data_from_body_endpoint(asset_template_id: int) -> str:
        return f'{HOST}/ES/AssetTemplates/{asset_template_id}/avatar/upload/fromBody'

    @staticmethod
    def delete_avatar_from_asset_template_by_id_endpoint(asset_template_id: int) -> str:
        return f'{HOST}/ES/AssetTemplates/{asset_template_id}/avatar'

    delete_avatar_from_assets_template_by_list_endpoint = f'{HOST}/ES/AssetTemplates/avatar'
    get_list_asset_templates_endpoint = f'{HOST}/ES/AssetTemplates'
    put_update_asset_templates_endpoint = f'{HOST}/ES/AssetTemplates'
    post_add_asset_templates_endpoint = f'{HOST}/ES/AssetTemplates'
    delete_asset_templates_by_list_endpoint = f'{HOST}/ES/AssetTemplates'

    @staticmethod
    def get_asset_template_by_id_endpoint(asset_template_id: int) -> str:
        return f'{HOST}/ES/AssetTemplates/{asset_template_id}'

    @staticmethod
    def delete_asset_template_by_id_endpoint(asset_template_id: int) -> str:
        return f'{HOST}/ES/AssetTemplates/{asset_template_id}'

    @staticmethod
    def get_list_districts_from_asset_template_endpoint(asset_template_id: int) -> str:
        return f'{HOST}/ES/AssetTemplates/{asset_template_id}/districts'

    @staticmethod
    def get_list_skills_from_asset_template_endpoint(asset_template_id: int) -> str:
        return f'{HOST}/ES/AssetTemplates/{asset_template_id}/skills'

    @staticmethod
    def get_list_work_types_from_asset_template_endpoint(asset_template_id: int) -> str:
        return f'{HOST}/ES/AssetTemplates/{asset_template_id}/workTypes'
