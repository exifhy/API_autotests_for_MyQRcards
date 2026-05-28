import time


class Payloads:
    @staticmethod
    def build_accounts_custom_message_template_update_payload(template_id: int) -> dict:
        suffix = int(time.time())
        return {
            "ID": int(template_id),
            "subjectTemplate": f"AT updated subject template {suffix}",
            "contentTemplate": (
                f"<h3>Обновленный шаблон {suffix}</h3>"
                f"<p>Здравствуйте, <b>@Model.ContactFirstName</b>, пишет @Model.UserFirstName.</p>"
            ),
        }
