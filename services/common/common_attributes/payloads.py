

class Payloads:

    @staticmethod
    def post_add_method_attributes_type_str_payloads(
            attribute_name: str,
            attribute_type_id: int,
            for_task: bool,
            for_asset: bool,
            for_check_list: bool,
            fro_complete_work: bool,
            for_contract: bool,
            for_company: bool
    ) -> list:
        payload = [
            {
                "name": attribute_name,
                "attributeTypeID": attribute_type_id,
                "isPublic": True,
                "measurementUnitID": None,
                "isRelevantForTask": for_task,
                "isRelevantForAsset": for_asset,
                "isRelevantForCheckList": for_check_list,
                "isRelevantForCompletedWork": fro_complete_work,
                "isRelevantForContract": for_contract,
                "isRelevantForCompany": for_company
            }
        ]
        return payload

    @staticmethod
    def post_add_attribute_to_user_payloads(
            attribute_name: str,
            attribute_type_id: int,
            customer: bool,
            stuff: bool
    ) -> list:
        payload = [
            {
                "name": attribute_name,
                "attributeTypeID": attribute_type_id,
                "isPublic": False,
                "IsRelevantForCustomer": customer,
                "IsRelevantForTechnician": stuff,
            }
        ]
        return payload

    @staticmethod
    def put_update_method_attributes_payloads(
            attribute_id: int,
            attribute_name: str,
            attribute_type_id: int,
            customer: bool,
            stuff: bool
    ) -> list:
        payload = [
            {
                "id": attribute_id,
                "name": attribute_name,
                "attributeTypeID": attribute_type_id,
                "isPublic": False,
                "IsRelevantForCustomer": customer,
                "IsRelevantForTechnician": stuff,
            }
        ]
        return payload

    @staticmethod
    def delete_method_attribute_payload(*args) -> list:
        return [*args]
