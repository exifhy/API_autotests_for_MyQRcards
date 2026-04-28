import time


class Payloads:
    @staticmethod
    def build_accounts_custom_message_template_payload() -> dict:
        suffix = int(time.time())
        return {
            "subjectTemplate": f"AT subject template {suffix}",
            "contentTemplate": (
                f"Здравствуйте, <b>@Model.ContactFirstName</b>. "
                f"Это тестовый шаблон {suffix} для @Model.UserFirstName."
            ),
        }
