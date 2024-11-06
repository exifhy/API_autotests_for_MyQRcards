

class Payloads:

    @staticmethod
    def attachments_and_asset_payloads(asset_id: int, *args) -> list:
        payload = [
            {
                "assetID": asset_id,
                "data": [
                    *args
                ]
            }
        ]
        return payload

