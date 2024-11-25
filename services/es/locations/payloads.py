

class Payloads:

    @staticmethod
    def add_location_payload(**kwargs) -> list:
        payload = [kwargs]
        return payload

    @staticmethod
    def delete_locations_payload(*args) -> list:
        return [*args]

