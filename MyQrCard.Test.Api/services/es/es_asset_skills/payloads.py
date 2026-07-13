

class Payloads:

    @staticmethod
    def skills_and_one_asset_payload(asset_id: int, *skill_ids: int) -> list:
        payload = [{
            "assetID": asset_id,
            "data": [skill_id for skill_id in skill_ids]
        }]
        return payload
