from src.utils.randoms import rand_word


class Payloads:
    @staticmethod
    def build_location_create_payload() -> dict:
        suffix = rand_word("loc", 8).replace("loc_", "")
        return {
            "Country": "Russia",
            "PostalCode": "190000",
            "Region": "Saint Petersburg",
            "City": "Saint Petersburg",
            "Address": f"Nevsky prospect {suffix}",
            "Notes": f"AT location {suffix}",
            "Latitude": 59.9343,
            "Longitude": 30.3351,
        }
