

class Payloads:

    @staticmethod
    def post_preferred_technicians_payload(asset_id: int, *user_ids: int) -> list:
        payload = [
            {
                "assetID": asset_id,
                "data": [
                    *user_ids
                ]
            }
        ]
        return payload
