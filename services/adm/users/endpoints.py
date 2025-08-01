from config.config import HOST


class Endpoints:

    @staticmethod
    def get_user_asset_assignments_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}/assetAssignments'

    @staticmethod
    def get_user_asset_list_queries_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}/assetListQueries'

    get_list_asset_queries_to_current_user_endpoint = f'{HOST}/ADM/users/this/AssetListQueries'
    get_users_short_list_endpoint = f'{HOST}/ADM/Users/short'
    get_list_users_endpoint = f'{HOST}/ADM/Users'
    head_users_endpoint = f'{HOST}/ADM/Users'
    add_users_endpoint = f'{HOST}/ADM/Users'
    delete_users_by_list_endpoint = f'{HOST}/ADM/Users'
    get_users_relevance_endpoint = f'{HOST}/ADM/Users/relevance'

    get_user_profile_endpoint = f'{HOST}/ADM/Users/profile'
    post_add_user_by_integration_endpoint = f'{HOST}/ADM/Users/addbyintegration'
    post_change_to_customer_endpoint = f'{HOST}/ADM/Users/changeToCustomer'
    post_change_to_staff_endpoint = f'{HOST}/ADM/Users/changeToStaff'

    @staticmethod
    def delete_user_by_id_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}'

    @staticmethod
    def put_restore_user_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}/restore'

    put_restore_users_endpoint = f'{HOST}/ADM/Users/restore'

    @staticmethod
    def get_user_districts_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}/districts'

    @staticmethod
    def put_resend_user_invitation_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}/resendinvitation'

    get_current_user_ui_permissions_endpoint = f'{HOST}/ADM/Users/this/permissions/ui'
    get_current_user_ext_permissions_endpoint = f'{HOST}/ADM/Users/this/permissions/ext'

    @staticmethod
    def get_user_profile_by_id_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}/profile'

    get_current_user_profile_endpoint = f'{HOST}/ADM/Users/this/profile'

    @staticmethod
    def put_upload_user_avatar_from_form_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}/avatar/upload/fromForm'

    @staticmethod
    def put_upload_user_avatar_from_body_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}/avatar/upload/fromBody'

    put_upload_current_user_avatar_from_form_endpoint = f'{HOST}/ADM/Users/this/avatar/upload/fromForm'
    put_upload_current_user_avatar_from_body_endpoint = f'{HOST}/ADM/Users/this/avatar/upload/fromBody'

    @staticmethod
    def delete_user_avatar_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}/avatar'

    delete_current_user_avatar_endpoint = f'{HOST}/ADM/Users/this/avatar'
    delete_users_avatar_endpoint = f'{HOST}/ADM/Users/avatar'

    @staticmethod
    def get_user_ratings_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}/ratings'

    post_user_registration_endpoint = f'{HOST}/ADM/Users/registration'
    post_user_registration_verify_endpoint = f'{HOST}/ADM/Users/registration/verify'
    post_add_api_user_in_tenant_endpoint = f'{HOST}/ADM/Users/api'
    post_add_anonymous_user_endpoint = f'{HOST}/ADM/Users/anonymous'

    @staticmethod
    def get_user_skills_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}/skills'

    @staticmethod
    def get_user_tags_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}/tags'

    @staticmethod
    def get_user_task_list_queries_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}/taskListQueries'

    get_current_user_task_list_queries_endpoint = f'{HOST}/ADM/Users/this/taskListQueries'

    @staticmethod
    def get_user_notifications_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}/notifications'

    get_current_user_notifications_endpoint = f'{HOST}/ADM/Users/this/notifications'

    @staticmethod
    def get_user_info_by_id_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}'

    @staticmethod
    def put_update_user_info_by_id_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}'

    @staticmethod
    def get_users_roles_by_id_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}/roles'

    @staticmethod
    def get_users_warehouses_by_user_id_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM//Users/{user_id}/warehouses'

    post_add_attributes_to_users_endpoint = f'{HOST}/ADM/Users/attributes'
    get_attributes_from_users_endpoint = f'{HOST}/ADM/Users/attributes'
    put_update_users_attributes_endpoint = f'{HOST}/ADM/Users/attributes'
    delete_attributes_from_users_endpoint = f'{HOST}/ADM/Users/attributes'

    @staticmethod
    def post_add_attributes_to_user_by_id_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM//Users/{user_id}/attributes'

    @staticmethod
    def get_attributes_from_user_by_id_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM//Users/{user_id}/attributes'

    @staticmethod
    def put_update_user_attributes_by_id_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM//Users/{user_id}/attributes'

    @staticmethod
    def delete_attributes_from_user_by_id_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM//Users/{user_id}/attributes'
