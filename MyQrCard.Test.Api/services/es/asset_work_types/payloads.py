

class Payloads:

    @staticmethod
    def asset_work_types_payload(asset_id: int, work_type_id: int) -> dict:
        payload = {
            "assetID": asset_id,
            "data": [
                work_type_id
            ]
        }
        return payload
