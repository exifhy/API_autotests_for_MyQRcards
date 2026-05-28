from src.utils.randoms import rand_hex_color


class Payloads:
    @staticmethod
    def build_company_designsettings_payload() -> dict:
        return {
            "Color": rand_hex_color(),
            "QRColor": rand_hex_color(),
            "BackgroundAttachmentID": None,
        }
