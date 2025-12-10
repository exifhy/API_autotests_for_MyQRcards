from config.config import HOST


class Endpoints:

    @staticmethod
    def get_list_materials_attachments_by_material_id_endpoint(material_id: int) -> str:
        return f'{HOST}/WH/Materials/{material_id}/attachments'

    @staticmethod
    def post_bind_materials_attachments_by_id_endpoint(material_id: int) -> str:
        return f'{HOST}/WH/Materials/{material_id}/attachments'

    @staticmethod
    def delete_materials_attachments_by_list_endpoint(material_id: int) -> str:
        return f'{HOST}/WH/Materials/{material_id}/attachments'

    @staticmethod
    def get_material_attachment_by_id_endpoint(material_id: int, attachment_id: int) -> str:
        return f'{HOST}/WH/Materials/{material_id}/attachment/{attachment_id}'

    @staticmethod
    def delete_material_attachment_by_id_endpoint(material_id: int, attachment_id: int) -> str:
        return f'{HOST}/WH/Materials/{material_id}/attachment/{attachment_id}'

    @staticmethod
    def get_temporary_redirect_material_attachments_by_id_endpoint(material_id: int, attachment_id: int) -> str:
        return f'{HOST}/WH/Materials/{material_id}/attachments/{attachment_id}'

    @staticmethod
    def post_upload_material_attachments_from_form_endpoint(material_id: int) -> str:
        return f'{HOST}/WH/Materials/{material_id}/attachments/upload/fromForm'

    @staticmethod
    def post_upload_material_attachments_from_body_endpoint(material_id: int) -> str:
        return f'{HOST}/WH/Materials/{material_id}/attachments/upload/fromBody'

    @staticmethod
    def get_list_barcodes_materials_by_id_endpoint(material_id: int) -> str:
        return f'{HOST}/WH/Materials/{material_id}/barcodes'

    put_update_barcodes_materials_endpoint = f'{HOST}/WH/Materials/barcodes'
    post_add_barcodes_materials_endpoint = f'{HOST}/WH/Materials/barcodes'
    delete_barcodes_materials_endpoint = f'{HOST}/WH/Materials/barcodes'

    @staticmethod
    def delete_barcodes_materials_by_id_endpoint(material_id: int, barcode_id: int) -> str:
        return f'{HOST}/WH/Materials/{material_id}/barcodes/{barcode_id}'

    get_list_materials_endpoint = f'{HOST}/WH/Materials'
    put_update_materials_endpoint = f'{HOST}/WH/Materials'
    post_add_materials_endpoint = f'{HOST}/WH/Materials'
    delete_materials_endpoint = f'{HOST}/WH/Materials'
    head_materials_endpoint = f'{HOST}/WH/Materials'
    get_list_required_materials_endpoint = f'{HOST}/WH/Materials/required'

    # @staticmethod
    # def get_list_required_materials_endpoint(required: int) -> str:
    #     return f'{HOST}/WH/Materials/{required}'

    @staticmethod
    def get_materials_by_id_endpoint(material_id: int) -> str:
        return f'{HOST}/WH/Materials/{material_id}'

    @staticmethod
    def delete_material_by_id_endpoint(material_id: int) -> str:
        return f'{HOST}/WH/Materials/{material_id}'

    get_list_materials_v2_endpoint = f'{HOST}/WH/Materials/v2'
    put_materials_restore_by_list_endpoint = f'{HOST}/WH/Materials/restore'

    @staticmethod
    def put_material_restore_by_id_endpoint(material_id: int) -> str:
        return f'{HOST}/WH/Materials/{material_id}/restore'
