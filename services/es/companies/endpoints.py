from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    @staticmethod
    def get_list_attachments_from_company_endpoint(company_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}/attachments/'

    @staticmethod
    def get_download_attachment_from_company_endpoint(company_id: int, attachment_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}/attachments/{attachment_id}'

    @staticmethod
    def get_info_attachment_from_company_by_id_endpoint(company_id: int, attachment_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}/attachment/{attachment_id}'

    @staticmethod
    def get_attributes_from_company_endpoint(company_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}/attributes'

    @staticmethod
    def post_add_attributes_to_company_endpoint(company_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}/attributes'

    @staticmethod
    def get_bank_accounts_from_company_endpoint(company_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}/bankAccounts'

    @staticmethod
    def put_update_bank_accounts_by_company_endpoint(company_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}/bankAccounts'

    @staticmethod
    def post_add_bank_accounts_to_company_endpoint(company_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}/bankAccounts'

    @staticmethod
    def delete_bank_accounts_from_company_by_list_endpoint(company_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}/bankAccounts'

    @staticmethod
    def delete_bank_account_from_company_by_id_endpoint(company_id: int, bank_account_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}/bankAccounts/{bank_account_id}'

    @staticmethod
    def get_list_contacts_from_company_endpoint(company_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}/contacts'

    @staticmethod
    def get_contact_from_company_by_id_endpoint(company_id: int, contact_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}/contacts/{contact_id}'

    @staticmethod
    def post_add_contact_to_company_by_id_endpoint(company_id: int, contact_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}/contacts/{contact_id}'

    @staticmethod
    def delete_contact_from_company_by_id_endpoint(company_id: int, contact_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}/contacts/{contact_id}'

    post_add_contacts_to_company_endpoint = f'{HOST}/ES/Companies/contacts'
    delete_contacts_from_company_endpoint = f'{HOST}/ES/Companies/contacts'
    get_list_companies_endpoint = f'{HOST}/ES/Companies/'
    put_update_company_endpoint = f'{HOST}/ES/Companies'
    post_add_company_endpoint = f'{HOST}/ES/Companies'
    delete_companies_endpoint = f'{HOST}/ES/Companies'
    head_companies_endpoint = f'{HOST}/ES/Companies'

    @staticmethod
    def delete_company_by_id_endpoint(company_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}'

    @staticmethod
    def get_company_by_id_endpoint(company_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}'

    put_restore_companies_by_list_endpoint = f'{HOST}/ES/Companies/restore'
    get_dadata_find_company_endpoint = f'{HOST}/ES/Companies/dadata/find'

    @staticmethod
    def get_actual_locations_from_company(company_id: int) -> str:
        return f'{HOST}/ES/Companies/{company_id}/locations/actual'
