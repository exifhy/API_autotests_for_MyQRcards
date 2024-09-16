

class Payloads:

    @staticmethod
    def add_user_customer_payload(
            name: str,
            surname: str,
            email: str,
            phone: str
    ) -> dict:
        payload = {
            "FirstName": name,
            "LastName": surname,
            "SexID": "1",
            "Email": email,
            "MobilePhone": phone,
            "WorkPhone": None,
            "OtherPhone": None,
            "VerificationCodeHash": "",
            "IsTechnician": False,
            "isTeam": False,
            "isCustomer": True,
            "MobilityID": 1,
            "geotrackingModeID": 3,
            "banReasonID": None,
            "BanTill": None
        }
        return payload

    @staticmethod
    def add_user_staff_payload(
            name: str,
            surname: str,
            email: str,
            phone: str
    ) -> dict:
        payload = {
            "firstName": name,
            "lastName": surname,
            "sexID": "1",
            "email": email,
            "mobilePhone": phone,
            "geotrackingModeID": "3",
            "isTechnician": False,
            "mobilityID": 1,
            "rate": None,
            "rateCurrencyID": 1
        }
        return payload

    @staticmethod
    def put_update_user_payload(
            name: str,
            surname: str,
            old_mail: str,
            old_phone: str,
            sex: str,
            email: str,
            phone: str
    ) -> dict:
        payload = {
            "firstName": name,
            "lastName": surname,
            "sexID": sex,
            "oldEmail": old_mail,
            "oldMobilePhone": old_phone,
            "email": email,
            "mobilePhone": phone,
            "geotrackingModeID": "3",
            "isTechnician": False,
            "mobilityID": 1,
            "rate": None,
            "rateCurrencyID": 1
        }
        return payload
