

class Payloads:

    @staticmethod
    def post_update_attributes_assets_payload(
            asset_id: int,
            attribute_id: int,
            value: str
    ) -> list:
        payload = [
            {
                "assetID": asset_id,
                "data": [
                    {
                        "attributeID": attribute_id,
                        "value": value,
                        "isPublic": True,
                        "sortOrder": 0
                    }
                ]
            }
        ]
        return payload
