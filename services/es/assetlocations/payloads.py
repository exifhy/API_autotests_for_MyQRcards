

class Payloads:

    @staticmethod
    def add_location_to_object_payload(asset_id: int, location_id: int) -> dict:
        payload = {
            "assetID": asset_id,
            "locationID": location_id
        }
        return payload
