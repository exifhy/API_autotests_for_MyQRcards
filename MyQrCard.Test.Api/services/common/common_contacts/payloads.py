

class Payloads:

    @staticmethod
    def post_add_contacts(
            full_name: str,
            email: str,
            phone: str,
            desc: str,
            position: str,
            **kwargs
    ) -> list:
        payload = [
            {
                "fullName": full_name,
                "email": email,
                "phone": phone,
                "position": position,
                "description": desc
            }
        ]
        if kwargs:
            payload.append(kwargs)
        return payload

    @staticmethod
    def put_update_contacts(
            contact_id: int,
            full_name: str,
            email: str,
            phone: str,
            desc: str,
            position: str,
            **kwargs
    ) -> list:
        payload = [
            {
                "id": contact_id,
                "fullName": full_name,
                "email": email,
                "phone": phone,
                "position": position,
                "description": desc
            }
        ]
        if kwargs:
            payload.append(kwargs)
        return payload

    @staticmethod
    def delete_mass_of_contact_payload(*args) -> list:
        return [*args]

