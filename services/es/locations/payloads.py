

class Payloads:

    @staticmethod
    def add_location_payload(**kwargs) -> list:
        payload = [kwargs]
        return payload

    @staticmethod
    def delete_locations_payload(*locations_ids: int) -> list:
        return list(locations_ids)

