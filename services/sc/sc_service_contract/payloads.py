

class Payloads:

    @staticmethod
    def post_method_for_add_contract_payload(
            company_id: int,
            contract_name: str,
            date_from: str,
            desc: str,
            conditions: str,
            **kwargs
    ) -> list:
        payload = [
            {
                "companyID": company_id,
                "remindExpirationDate": False,
                "name": contract_name,
                "dateFrom": date_from,
                "dateTill": None,
                "description": desc,
                "agreementConditions": conditions,
                "reminderDate": None
            }
        ]
        if kwargs:
            payload.append(kwargs)
        return payload

    @staticmethod
    def delete_mass_of_contract_payload(*args) -> list:
        return [*args]

    @staticmethod
    def post_add_list_object_to_contract_payload(asset_id: int, child: bool, **kwargs) -> list:
        payload = [
            {
                "assetID": asset_id,
                "includeChildren": child
            }
        ]
        if kwargs:
            payload.append(kwargs)
        return payload

    @staticmethod
    def put_method_for_update_contract_payload(
            contract_id: int,
            company_id: int,
            contract_name: str,
            date_from: str,
            desc: str,
            conditions: str,
            **kwargs
    ) -> list:
        payload = [
            {
                "id": contract_id,
                "companyID": company_id,
                "remindExpirationDate": False,
                "name": contract_name,
                "dateFrom": date_from,
                "dateTill": None,
                "description": desc,
                "agreementConditions": conditions,
                "reminderDate": None
            }
        ]
        if kwargs:
            payload.append(kwargs)
        return payload
