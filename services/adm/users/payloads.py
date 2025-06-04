

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
            "isTechnician": True,
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
            sex,
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

    @staticmethod
    def delete_users_by_list_payload(*user_ids: int):
        return [*user_ids]

    @staticmethod
    def post_change_status_users_by_list_payload(*user_ids: int):
        return [*user_ids]

    @staticmethod
    def put_restore_users_by_list_payload(*user_ids: int):
        return [*user_ids]

    @staticmethod
    def delete_users_avatar_by_list_payload(*user_ids: int):
        return [*user_ids]

    @staticmethod
    def post_add_users_registration_payload(
            invitation_id: str,
            name: str,
            surname: str,
            email: str
    ) -> dict:
        payload = {
            "invitationID": invitation_id,
            "firstName": name,
            "lastName": surname,
            "email": email
        }
        return payload

    @staticmethod
    def post_add_users_registration_verify_payload(tenant_id, account_id: int) -> dict:
        payload = {
            "tenantID": tenant_id,
            "accountID": account_id
        }
        return payload

