
class Payloads:
    @staticmethod
    def build_subscription_designsettings_merge_payload(
        *,
        color: str | None = None,
        qr_color: str | None = None,
        background_color: str | None = None,
        foreground_color: str | None = None,
    ) -> dict:
        payload: dict[str, str] = {}
        if color is not None:
            payload["color"] = str(color)
        if qr_color is not None:
            payload["qrColor"] = str(qr_color)
        if background_color is not None:
            payload["backgroundColor"] = str(background_color)
        if foreground_color is not None:
            payload["foregroundColor"] = str(foreground_color)
        return payload
