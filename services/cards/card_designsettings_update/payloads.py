
class Payloads:
    @staticmethod
    def build_card_designsettings_update_payload() -> dict:
        return {
            "color": "4673B4",
            "qrColor": "8E60DD",
            "backgroundColor": "8B3FFD",
            "foregroundColor": "1D1D1D",
        }

    @staticmethod
    def build_card_designsettings_font_payload(font_color: str, font_style_id: int) -> dict:
        return {
            "fontColor": font_color,
            "fontStyleID": font_style_id,
        }
