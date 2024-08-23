
class Payloads:

    @staticmethod
    def object_creation_payload(
            parent_id: int,
            name: str,
            company_id: int,
            asset_type_id: int,
            asset_class_is: int,
            schedule_rule_id: int,
    ):
        payload = {
            "parentID": parent_id,
            "name": name,
            "companyID": company_id,
            "assetTypeID": asset_type_id,
            "assetClassID": asset_class_is,
            "checkListID": None,
            "responsiblePerson": None,
            "scheduleRuleID": schedule_rule_id,
            "warrantyTill": None,
            "notes": "Объект",
            "isMobileAsset": False,
            "isInheritParentDistricts": True,
            "isSkipForEscalation": False,
            "isStopEscalation": False,
            "isAutoPublish": True,
            "positionOnSchema": None
        }
        return payload
