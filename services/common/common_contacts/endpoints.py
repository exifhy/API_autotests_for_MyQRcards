from config.config import HOST


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
