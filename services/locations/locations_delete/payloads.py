
class Payloads:
    @staticmethod
    def build_locations_delete_payload(location_ids: list[int]) -> list[int]:
        return [int(location_id) for location_id in location_ids]
