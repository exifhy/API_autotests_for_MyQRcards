from http import HTTPStatus

import allure
import pytest

from services.companies.company_delete_by_id.api_company_delete_by_id import CompanyDeleteByIdAPI
from services.companies.company_email_signature_settings_by_id.api_company_email_signature_settings_by_id import (
    CompanyEmailSignatureSettingsByIdAPI,
)
from services.companies.company_email_signature_settings_delete.api_company_email_signature_settings_delete import (
    CompanyEmailSignatureSettingsDeleteAPI,
)
from services.companies.company_email_signature_settings_update.api_company_email_signature_settings_update import (
    CompanyEmailSignatureSettingsUpdateAPI,
)
from services.companies.company_email_signature_settings_update.payloads import Payloads


@allure.epic("API")
@allure.feature("Companies")
@pytest.mark.api
@pytest.mark.company
@allure.description(
    """
    REQUIREMENT 32677 — хранение настроек email-подписи компании.
    /Companies/{companyID}/emailsignaturesettings (GET/PUT/DELETE)
    """
)
class TestCompanyEmailSignatureSettings:
    @allure.title("GET без сохранённых настроек -> 204, пустое тело")
    def test_get_no_settings_returns_204(self, created_company):
        company_id = created_company["id"]

        model = CompanyEmailSignatureSettingsByIdAPI().get_email_signature_settings(company_id)

        assert model is None

    @allure.title("PUT сохраняет настройки -> GET возвращает 200 с теми же значениями")
    @pytest.mark.smoke
    def test_put_then_get_returns_saved_settings(self, created_company):
        company_id = created_company["id"]
        payload = Payloads.build_email_signature_settings_payload(
            show_position=False,
            show_phone=False,
            show_logo=False,
            qr_size=150,
            greeting_text="AT probe greeting",
        )

        response = CompanyEmailSignatureSettingsUpdateAPI().update_email_signature_settings(company_id, payload)
        assert response.status_code == HTTPStatus.ACCEPTED

        model = CompanyEmailSignatureSettingsByIdAPI().get_email_signature_settings(company_id)

        assert model is not None
        assert model.companyID == company_id
        assert model.showGreeting == payload["showGreeting"]
        assert model.showName == payload["showName"]
        assert model.showPosition == payload["showPosition"]
        assert model.showCompany == payload["showCompany"]
        assert model.showPhone == payload["showPhone"]
        assert model.showEmail == payload["showEmail"]
        assert model.showQR == payload["showQR"]
        assert model.showLogo == payload["showLogo"]
        assert model.qrSize == payload["qrSize"]
        assert model.greetingText == payload["greetingText"]

    @allure.title("Повторный PUT полностью заменяет настройки, старые значения не остаются")
    def test_put_fully_replaces_previous_settings(self, created_company):
        company_id = created_company["id"]
        first_payload = Payloads.build_email_signature_settings_payload(
            show_position=True, qr_size=180, greeting_text="First"
        )
        CompanyEmailSignatureSettingsUpdateAPI().update_email_signature_settings(company_id, first_payload)

        second_payload = Payloads.build_email_signature_settings_payload(
            show_greeting=False,
            show_name=False,
            show_position=False,
            show_company=False,
            show_phone=False,
            show_email=False,
            show_qr=False,
            show_logo=False,
            qr_size=60,
            greeting_text="",
        )
        CompanyEmailSignatureSettingsUpdateAPI().update_email_signature_settings(company_id, second_payload)

        model = CompanyEmailSignatureSettingsByIdAPI().get_email_signature_settings(company_id)

        assert model is not None
        assert model.showGreeting is False
        assert model.showName is False
        assert model.showPosition is False
        assert model.showCompany is False
        assert model.showPhone is False
        assert model.showEmail is False
        assert model.showQR is False
        assert model.showLogo is False
        assert model.qrSize == 60
        assert model.greetingText == ""

    @allure.title("DELETE удаляет настройки -> следующий GET снова 204")
    @pytest.mark.smoke
    def test_delete_then_get_returns_204(self, created_company):
        company_id = created_company["id"]
        CompanyEmailSignatureSettingsUpdateAPI().update_email_signature_settings(
            company_id, Payloads.build_email_signature_settings_payload()
        )

        response = CompanyEmailSignatureSettingsDeleteAPI().delete_email_signature_settings(company_id)
        assert response.status_code == HTTPStatus.ACCEPTED

        model = CompanyEmailSignatureSettingsByIdAPI().get_email_signature_settings(company_id)
        assert model is None

    @allure.title("DELETE без сохранённых настроек — тоже 202 (идемпотентно)")
    def test_delete_when_nothing_saved_still_202(self, created_company):
        company_id = created_company["id"]

        response = CompanyEmailSignatureSettingsDeleteAPI().delete_email_signature_settings(company_id)

        assert response.status_code == HTTPStatus.ACCEPTED

    @allure.title("GET/PUT/DELETE без авторизации -> 401")
    def test_without_auth_401(self, created_company):
        company_id = created_company["id"]

        get_response = CompanyEmailSignatureSettingsByIdAPI().get_email_signature_settings_without_auth(company_id)
        assert get_response.status_code == HTTPStatus.UNAUTHORIZED

        put_response = CompanyEmailSignatureSettingsUpdateAPI().update_email_signature_settings_without_auth(
            company_id, Payloads.build_email_signature_settings_payload()
        )
        assert put_response.status_code == HTTPStatus.UNAUTHORIZED

        delete_response = CompanyEmailSignatureSettingsDeleteAPI().delete_email_signature_settings_without_auth(
            company_id
        )
        assert delete_response.status_code == HTTPStatus.UNAUTHORIZED

    @allure.title("Удалённая компания: GET/PUT emailsignaturesettings -> 403")
    def test_deleted_company_returns_403(self, created_company):
        """Комментарий к REQUIREMENT 32677 утверждает 409 для удалённой компании,
        но живая проверка на dev показала 403 Forbidden (тот же код, что и для
        компании без доступа) — расхождение задокументировано в чек-листе задачи."""
        company_id = created_company["id"]
        CompanyDeleteByIdAPI().delete_company_by_id(company_id)

        get_response = CompanyEmailSignatureSettingsByIdAPI().get_email_signature_settings_raw(company_id)
        assert get_response.status_code == HTTPStatus.FORBIDDEN

        put_response = CompanyEmailSignatureSettingsUpdateAPI().update_email_signature_settings_raw(
            company_id, Payloads.build_email_signature_settings_payload()
        )
        assert put_response.status_code == HTTPStatus.FORBIDDEN

    @allure.title("qrSize вне диапазона 60-200 -> бэк не валидирует, сохраняется как есть")
    def test_qr_size_out_of_range_not_validated(self, created_company):
        company_id = created_company["id"]
        payload = Payloads.build_email_signature_settings_payload(qr_size=999)

        response = CompanyEmailSignatureSettingsUpdateAPI().update_email_signature_settings(company_id, payload)
        assert response.status_code == HTTPStatus.ACCEPTED

        model = CompanyEmailSignatureSettingsByIdAPI().get_email_signature_settings(company_id)
        assert model is not None
        assert model.qrSize == 999
