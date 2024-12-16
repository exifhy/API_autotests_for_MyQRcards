

class Payloads:

    @staticmethod
    def post_add_company_locations_payload(company_id: int, location_id: int) -> dict:
        payload = {
            "companyID": company_id,
            "locationID": location_id
        }
        return payload

    @staticmethod
    def put_update_location_from_company_payload(company_id: int, location_id: int) -> dict:
        payload = {
            "companyID": company_id,
            "locationID": location_id
        }
        return payload

    @staticmethod
    def delete_location_from_company_payload(company_id: int) -> dict:
        payload = {
            "companyID": company_id,
        }
        return payload
