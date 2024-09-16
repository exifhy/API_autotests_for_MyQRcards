

class Payloads:

    @staticmethod
    def add_during_day_schedule_for_tenant_payload(
            date_from: str,
            date_till: str
    ) -> list:
        payload = [
            {
                "frequencyTypeID": "1",
                "options": {
                    "Name": "During the day",
                    "DateFrom": date_from,
                    "DateTill": date_till,
                    "Frequency": {
                        "AppointmentTimes": ["07:00"]
                    }
                }
            }
        ]
        return payload

