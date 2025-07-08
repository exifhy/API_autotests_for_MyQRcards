from config.config import HOST


class Endpoints:

    get_list_notifications_fields_endpoint = f'{HOST}/MSG/Notifications/fields'
    post_add_notifications_endpoint = f'{HOST}/MSG/Notifications'
    get_list_notifications_endpoint = f'{HOST}/MSG/Notifications'
    head_notifications_endpoint = f'{HOST}/MSG/Notifications'
    put_update_notifications_endpoint = f'{HOST}/MSG/Notifications'
    put_update_all_notifications_endpoint = f'{HOST}/MSG/Notifications/all'
