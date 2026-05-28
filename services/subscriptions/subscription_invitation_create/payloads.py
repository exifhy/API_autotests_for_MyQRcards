from src.utils.randoms import rand_email, rand_name, rand_phone_ru8


class Payloads:
    @staticmethod
    def build_subscription_invitation_payload(
        *,
        company_id: int,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        position: str = "Director",
        is_accept_advertising: bool = False,
    ) -> dict:
        return {
            "Email": email or rand_email(domain="mail.com"),
            "FirstName": first_name or rand_name("AT_FN"),
            "LastName": last_name or rand_name("AT_LN"),
            "CompanyID": int(company_id),
            "Phone": phone or rand_phone_ru8(),
            "Position": position,
            "IsAcceptAdvertising": bool(is_accept_advertising),
        }
