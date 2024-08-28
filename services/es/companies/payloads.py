

class Payloads:

    @staticmethod
    def add_companies_payload(name: str, type_id: int) -> list:
        payload = [
            {
                "name": name,
                "registrationTypeID": type_id,
                "isOurCompany": True
            }
        ]
        return payload

    @staticmethod
    def marks_company_as_remote(company_id: int) -> list:
        return [company_id]
