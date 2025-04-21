from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_add_contacts_endpoint = f'{HOST}/COMMON/contacts'
    get_list_info_contacts_endpoint = f'{HOST}/COMMON/contacts'
    put_update_contacts_endpoint = f'{HOST}/COMMON/contacts'
    delete_contacts_endpoint = f'{HOST}/COMMON/contacts'

    @staticmethod
    def get_info_contact_by_id(contact_id: int):
        return f'{HOST}/COMMON/contacts/{contact_id}'

    @staticmethod
    def delete_contact_by_id(contact_id: int):
        return f'{HOST}/COMMON/contacts/{contact_id}'
