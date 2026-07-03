

class Payloads:

    @staticmethod
    def post_bind_attachments_and_company_payload(company_id: int, *attachment_ids: int) -> list:
        payload = [
            {
                "companyID": company_id,
                "data": [
                    *attachment_ids
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_unbind_attachments_from_company_payload(company_id: int, *attachment_ids: int) -> list:
        payload = [
            {
                "companyID": company_id,
                "data": [
                    *attachment_ids
                ]
            }
        ]
        return payload

