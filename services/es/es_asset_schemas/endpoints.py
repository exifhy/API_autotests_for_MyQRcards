import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    @staticmethod
    def get_plan_scheme_attached_to_asset_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assetSchemas/asset/{asset_id}'

    @staticmethod
    def get_list_existing_asset_schemas_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assetSchemas/ascList/{asset_id}'

    @staticmethod
    def get_asset_schema_by_id_endpoint(schema_id: int) -> str:
        return f'{HOST}/ES/assetSchemas/{schema_id}'

    @staticmethod
    def delete_asset_schema_by_id_endpoint(schema_id: int) -> str:
        return f'{HOST}/ES/assetSchemas/{schema_id}'

    @staticmethod
    def put_update_asset_schemas_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assetSchemas/asset/{asset_id}'

    @staticmethod
    def post_add_asset_schemas_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assetSchemas/asset/{asset_id}'

    get_list_asset_schemas_endpoint = f'{HOST}/ES/assetSchemas/list'

    @staticmethod
    def post_bind_asset_schemas_to_asset_by_id_endpoint(schema_id: int) -> str:
        return f'{HOST}/ES/assetSchemas/{schema_id}/bind'

    @staticmethod
    def put_unbind_asset_schemas_from_asset_by_id_endpoint(schema_id: int) -> str:
        return f'{HOST}/ES/assetSchemas/{schema_id}/unbind'

    @staticmethod
    def get_data_image_bind_asset_schemas_by_id_endpoint(schema_id: int) -> str:
        return f'{HOST}/ES/assetSchemas/{schema_id}/image'

    @staticmethod
    def delete_image_bind_asset_schemas_by_id_endpoint(schema_id: int) -> str:
        return f'{HOST}/ES/assetSchemas/{schema_id}/image'

    @staticmethod
    def get_image_bind_asset_schemas_temporary_redirect_by_id_endpoint(schema_id: int) -> str:
        return f'{HOST}/ES/assetSchemas/{schema_id}/image/download'

    @staticmethod
    def get_temporary_redirect_to_link_for_download_attach_asset_schema_by_id_endpoint(schema_id: int) -> str:
        return f'{HOST}/ES/assetSchemas/{schema_id}/image/download'

    @staticmethod
    def post_upload_file_add_asset_schema_from_form_endpoint(schema_id: int) -> str:
        return f'{HOST}/ES/assetSchemas/{schema_id}/image/upload'

    @staticmethod
    def post_bind_image_to_asset_schema_by_id_endpoint(schema_id: int, attachment_id: int) -> str:
        return f'{HOST}/ES/assetSchemas/{schema_id}/image/attach/{attachment_id}'

    @staticmethod
    def get_list_points_from_asset_schema_endpoint(schema_id: int) -> str:
        return f'{HOST}/ES/assetSchemas/{schema_id}/points'

    @staticmethod
    def post_add_points_to_asset_schema_endpoint(schema_id: int) -> str:
        return f'{HOST}/ES/assetSchemas/{schema_id}/points'

    @staticmethod
    def delete_points_from_asset_schema_by_list_endpoint(schema_id: int) -> str:
        return f'{HOST}/ES/assetSchemas/{schema_id}/points'
