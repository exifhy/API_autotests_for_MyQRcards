

class Payloads:

    @staticmethod
    def post_add_license_tenant_payload() -> dict:
        payload = {
            "licenseID": 0,
            "dateFrom": "2025-04-22T09:54:12.971Z",
            "dateTill": "2025-04-22T09:54:12.971Z",
            "quantity": 0,
            "paymentInfo": {
                "payer": "string",
                "tin": "string",
                "iec": "string",
                "lawAddress": "string",
                "postAddress": "string",
                "phone": "string",
                "email": "string",
                "contactPerson": "string",
                "bic": "string",
                "bankName": "string",
                "correspondingAccount": "string",
                "checkingAccount": "string"
            }
        }
        return payload

    @staticmethod
    def delete_licenses_from_tenant_by_list_payload(*licenses_ids: int or tuple) -> list:
        return [*licenses_ids]

    @staticmethod
    def put_update_license_tenant_payload() -> dict:
        payload = {
            "licenseID": 0,
            "dateFrom": "2025-04-22T10:27:47.755Z",
            "dateTill": "2025-04-22T10:27:47.755Z",
            "quantity": 0,
            "id": 0
        }
        return payload

    @staticmethod
    def post_add_packages_to_db_cross_tenant_admin_payload() -> dict:
        payload = {
            "AddonID": "11 тест 08.04.25",
            "Version": "000011",
            "Name": "11",
            "IconUrl": "icon_url12222",
            "AddonUrl": "https://dev-automate.hubex.ru/webhook/18cfbdbe-f44d-498b-b3de-e04a0a94bb9f?reportID=aa234",
            "ResourceID": 2,
            "IsMobile": False
        }
        return payload

    @staticmethod
    def delete_packages_from_db_payload(addon_id: str, version: str) -> dict:
        payload = {
            "addonID": addon_id,
            "version": version
        }
        return payload

    @staticmethod
    def post_add_variables_to_tenant_payload(*data: dict or tuple):
        return [*data]

    @staticmethod
    def put_update_variables_tenant_payload(*data: dict or tuple):
        return [*data]

    @staticmethod
    def delete_variables_from_tenant_payload(*names: str or tuple):
        return [*names]
