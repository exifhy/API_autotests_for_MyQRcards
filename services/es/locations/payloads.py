

class Payloads:

    @staticmethod
    def add_location_payload(**kwargs) -> list:
        payload = [kwargs]
        return payload

    @staticmethod
    def put_update_location_payload(*params: dict) -> list:
        return [*params]

    @staticmethod
    def delete_locations_payload(*args) -> list:
        return [*args]

    @staticmethod
    def delete_locations_by_list_remove_payload(*args) -> list:
        return [*args]

