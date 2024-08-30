

class Payloads:

    @staticmethod
    def asset_districts_payload(asset_id: int, district_id: int) -> dict:
        payload = {
            "assetID": asset_id,
            "data": [
                {
                    "id": district_id
                }
            ]
        }
        return payload
