

class Payloads:

    @staticmethod
    def add_companies_payload(
            name: str,
            type_id: int,
            company_our: bool,
            company_contractor: bool,
            company_employer: bool
    ) -> list:
        payload = [
            {
                "name": name,
                "registrationTypeID": type_id,
                "isOurCompany": company_our,
                "isContractorHolder": company_contractor,
                "isEmployer": company_employer
            }
        ]
        return payload

    @staticmethod
    def delete_companies_by_list_payload(*company_ids: int) -> list:
        return [*company_ids]

    @staticmethod
    def update_companies_payload(
            company_id: int,
            company_name: str,
            company_email: str,
            company_contractor: bool,
            company_employer: bool,
            company_our: bool,
            company_phone: str,
            company_type: str,
            customer_id: int,
            staff_id: int
    ):
        payload = [
            {
                "id": company_id,
                "name": company_name,
                "email": company_email,
                "isContractorHolder": company_contractor,
                "isEmployer": company_employer,
                "isOurCompany": company_our,
                "phone": company_phone,
                "registrationTypeID": company_type,
                "customerOrgUnitID": customer_id,
                "staffOrgUnitID": staff_id
            }
        ]
        return payload

    @staticmethod
    def post_add_attributes_to_company_payload(*params: dict) -> list:
        return [*params]

    @staticmethod
    def put_update_bank_accounts_by_company_payload(*params: dict) -> list:
        return [*params]

    @staticmethod
    def post_add_bank_accounts_to_company_payload(*params: dict) -> list:
        return [*params]

    @staticmethod
    def delete_bank_accounts_from_company_by_list_payload(*bank_account_company_id: int) -> list:
        return [*bank_account_company_id]

    @staticmethod
    def post_add_contacts_to_company_payload(*params: dict) -> list:
        return [*params]

    @staticmethod
    def delete_contacts_from_company_by_list_payload(*params: dict) -> list:
        return [*params]

    @staticmethod
    def put_restore_companies_by_list_payload(*company_ids: int) -> list:
        return [*company_ids]


