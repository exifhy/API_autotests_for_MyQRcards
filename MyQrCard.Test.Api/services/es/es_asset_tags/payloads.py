

class Payloads:

    @staticmethod
    def post_add_tags_to_asset_payload(asset_id: int, *name: str) -> list:
        payload = [
            {
                "assetID": asset_id,
                "tags": [*name]
            }
        ]
        return payload

    @staticmethod
    def delete_tags_from_asset_payload(asset_id: int, *name: str) -> list:
        payload = [
            {
                "assetID": asset_id,
                "tags": [*name]
            }
        ]
        return payload
