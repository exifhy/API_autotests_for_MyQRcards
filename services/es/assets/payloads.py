
class Payloads:

    @staticmethod
    def object_creation_payload(
            parent_id: int or None,
            name: str,
            company_id: int,
            asset_type_id: int,
            asset_class_id: int,
            notes: str
    ) -> dict:
        payload = {
            "parentID": parent_id,
            "name": name,
            "companyID": company_id,
            "assetTypeID": asset_type_id,
            "assetClassID": asset_class_id,
            "checkListID": None,
            "responsiblePerson": None,
            "scheduleRuleID": None,
            "warrantyTill": None,
            "notes": notes,
            "isMobileAsset": False,
            "isInheritParentDistricts": True,
            "isSkipForEscalation": False,
            "isStopEscalation": False,
            "isAutoPublish": True,
            "positionOnSchema": None
        }
        return payload

    @staticmethod
    def delete_avatar_from_assets_payloads(*args) -> list:
        return [*args]

    @staticmethod
    def post_checklist_to_asset_payloads(*args) -> list:
        return [*args]

    @staticmethod
    def delete_checklists_from_asset_payloads(*args) -> list:
        return [*args]
