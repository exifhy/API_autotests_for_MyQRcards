import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_account_applications_endpoint = f'{HOST}/AUTH/Accounts/this/applications'
    put_updating_current_account_application_data_endpoint = f'{HOST}/AUTH/Accounts/this/applications'
    delete_unbind_app_device_from_your_current_account_endpoint = f'{HOST}/AUTH/Accounts/this/applications'
    post_logout_endpoint = f'{HOST}/AUTH/Accounts/logout'
    post_register_endpoint = f'{HOST}/AUTH/Accounts/register'
    get_accounts_endpoint = f'{HOST}/AUTH/Accounts'
    head_checks_if_account_is_present_by_specified_credentials_endpoint = f'{HOST}/AUTH/Accounts'
    get_list_notifications_from_log_endpoint = f'{HOST}/AUTH/Accounts/this/notifications'
