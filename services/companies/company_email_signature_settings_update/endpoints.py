from config.config import HOST


class Endpoints:
    update_company_email_signature_settings_endpoint = f"{HOST}/Companies/{{company_id}}/emailsignaturesettings"
