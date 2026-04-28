import time


class Payloads:
    @staticmethod
    def build_card_custom_message_templates_update_payload() -> dict:
        suffix = int(time.time())
        return {
            "subjectTemplate": f"AT custom subject {suffix}",
            "contentTemplate": (
                f"<h3>Здравствуйте, <b>@Model.ContactFirstName</b></h3>"
                f"<p>AT custom content {suffix} для <i>@Model.UserFirstName</i>.</p>"
            ),
        }
