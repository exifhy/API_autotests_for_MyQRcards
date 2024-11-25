

class Payloads:

    @staticmethod
    def add_districts_payload(asset_id: int, district_id: int) -> dict:
        payload = {
            "assetID": asset_id,
            "data": [
                {
                    "id": district_id
                },
                {
                    "id": 1
                }
            ]
        }
        return payload

    @staticmethod
    def add_default_districts_payload(asset_id: int) -> dict:
        payload = {
            "assetID": asset_id,
            "data": [
                {
                    "id": 1
                }
            ]
        }
        return payload

    @staticmethod
    def delete_districts_payload(asset_id: int, district_id: int) -> dict:
        payload = {
            "assetID": asset_id,
            "data": [
                district_id
            ]
        }
        return payload

    @staticmethod
    def add_new_districts_payload(asset_id: int, district_id: int) -> dict:
        payload = {
            "assetID": asset_id,
            "data": [
                {
                    "id": district_id
                }
            ]
        }
        return payload

    @staticmethod
    def add_new_districts_args_payload(asset_id: int, *district_ids: int) -> dict:
        payload = {
            "assetID": asset_id,
            "data": [{"id": district_id} for district_id in district_ids]
        }
        return payload
