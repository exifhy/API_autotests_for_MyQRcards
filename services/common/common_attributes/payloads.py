

class Payloads:

    @staticmethod
    def post_add_method_attributes_payloads(
            attribute_name: str,
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
                "attributeTypeID": 1,
                "isPublic": True,
                "measurementUnitID": 4,
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
    def delete_method_attribute_payload(*args) -> list:
        return [*args]

