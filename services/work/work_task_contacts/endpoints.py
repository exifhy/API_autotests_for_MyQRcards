import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_add_contacts_to_task_endpoint = f'{HOST}/WORK/taskContacts'
    delete_contacts_from_task_endpoint = f'{HOST}/WORK/taskContacts'
