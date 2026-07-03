

class Payloads:

    @staticmethod
    def post_clients_locations_payloads(time: str) -> list:
        payload = [
            {
            "Coordinate": "59.83252198416125:30.35860853992472",
            "Accuracy": 9.8399999999999999,
            "ClientTimestamp": time,
            "Altitude": 18.059999999999999,
            "Speed": -1,
            "is_mocked": False,
            "Bearing": -1
            }
        ]
        return payload