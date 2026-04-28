import time


class Payloads:
    @staticmethod
    def build_card_update_payload(*, company_id: int, gallery_attachment_ids: list[int] | None = None) -> dict:
        now = int(time.time())
        payload = {
            "name": f"AT_Card_Updated_{now}",
            "culture": "ru-RU",
            "isPrimary": True,
            "themeID": 2,
            "person": {
                "firstName": f"UFN_{now}",
                "lastName": f"ULN_{now}",
                "middleName": f"UMN_{now}",
            },
            "isHidden": False,
            "employment": {
                "companyID": int(company_id),
                "position": "AT Tester",
                "activity": "AT Update Activity",
            },
        }
        if gallery_attachment_ids:
            payload["person"]["attachments"] = [
                {"attachmentID": int(attachment_id), "sortOrder": index}
                for index, attachment_id in enumerate(gallery_attachment_ids, start=1)
            ]
        return payload
