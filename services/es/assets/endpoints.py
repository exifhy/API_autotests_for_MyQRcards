from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_directory_of_objects_available_to_user_endpoint = f'{HOST}/ES/assets'
    create_object_endpoint = f'{HOST}/ES/assets'
    head_asset_endpoint = f'{HOST}/ES/assets'
    put_update_asset_endpoint = f'{HOST}/ES/assets'
    delete_assets_by_list_endpoint = f'{HOST}/ES/assets'
    delete_assets_avatar_by_list_endpoint = f'{HOST}/ES/assets/avatar'
    post_add_contacts_to_asset_by_list_endpoint = f'{HOST}/ES/assets/contacts'
    delete_contacts_from_asset_by_list_endpoint = f'{HOST}/ES/assets/contacts'
    delete_assets_and_all_child_assets_by_list_endpoint = f'{HOST}/ES/assets/full'
    put_restore_assets_endpoint = f'{HOST}/ES/assets/restore'

    @staticmethod
    def get_list_assignments_asset_to_user_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/assignments'

    @staticmethod
    def get_list_attachments_bind_to_asset_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/attachments'

    @staticmethod
    def get_attachment_bind_to_asset_by_id_endpoint(asset_id: int, attachment_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/attachments/{attachment_id}'

    @staticmethod
    def get_list_of_user_attributes_by_asset_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/attributes'

    @staticmethod
    def put_upload_avatar_attachment_from_form_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/avatar/upload/fromForm'

    @staticmethod
    def put_upload_avatar_attachment_from_body_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/avatar/upload/fromBody'

    @staticmethod
    def delete_avatar_asset_by_id_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/avatar'

    @staticmethod
    def get_asset_checklist_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/checkLists'

    @staticmethod
    def post_add_checklists_to_asset_by_list_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/checkLists'

    @staticmethod
    def delete_checklist_from_asset_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/checkLists'

    @staticmethod
    def post_add_checklist_to_asset_by_id_endpoint(asset_id: int, checklist_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/checkLists/{checklist_id}'

    @staticmethod
    def delete_checklist_from_asset_by_id_endpoint(asset_id: int, checklist_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/checkLists/{checklist_id}'

    @staticmethod
    def get_list_valid_contacts_for_asset_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/contacts'

    @staticmethod
    def get_asset_contact_by_id_endpoint(asset_id: int, contact_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/contacts/{contact_id}'

    @staticmethod
    def post_add_contact_to_asset_endpoint(asset_id: int, contact_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/contacts/{contact_id}'

    @staticmethod
    def delete_contact_from_asset_by_id_endpoint(asset_id: int, contact_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/contacts/{contact_id}'

    @staticmethod
    def delete_object_by_id_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}'

    @staticmethod
    def detailed_information_on_object_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}'

    @staticmethod
    def method_of_publishing_an_object_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/publish'

    @staticmethod
    def put_of_unpublishing_an_object_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/unpublish'

    @staticmethod
    def delete_asset_and_all_child_assets_by_id_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/full'

    @staticmethod
    def update_object_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}'

    @staticmethod
    def get_list_districts_for_asset_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/districts'

    @staticmethod
    def get_actual_locations_asset_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/locations/actual'

    @staticmethod
    def get_asset_skills_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/skills'

    @staticmethod
    def get_active_tags_by_asset_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/tags'

    @staticmethod
    def get_list_work_types_by_asset_endpoint(asset_id: int) -> str:
        return f'{HOST}/ES/assets/{asset_id}/workTypes'
