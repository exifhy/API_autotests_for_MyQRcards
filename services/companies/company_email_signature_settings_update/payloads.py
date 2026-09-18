class Payloads:
    @staticmethod
    def build_email_signature_settings_payload(
        *,
        show_greeting: bool = True,
        show_name: bool = True,
        show_position: bool = True,
        show_company: bool = True,
        show_phone: bool = True,
        show_email: bool = True,
        show_qr: bool = True,
        show_logo: bool = True,
        qr_size: int = 120,
        greeting_text: str = "С уважением,",
    ) -> dict:
        return {
            "showGreeting": show_greeting,
            "showName": show_name,
            "showPosition": show_position,
            "showCompany": show_company,
            "showPhone": show_phone,
            "showEmail": show_email,
            "showQR": show_qr,
            "showLogo": show_logo,
            "qrSize": qr_size,
            "greetingText": greeting_text,
        }
