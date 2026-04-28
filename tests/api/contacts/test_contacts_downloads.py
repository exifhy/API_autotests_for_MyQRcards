import allure
import pytest
from http import HTTPStatus

from services.contacts.contact_download_by_id.api_contact_download_by_id import ContactDownloadByIdAPI
from services.contacts.contacts_download_csv.api_contacts_download_csv import ContactsDownloadCsvAPI


@allure.epic("API")
@allure.feature("Contacts")
@pytest.mark.api
@pytest.mark.contacts
class TestContactsDownloads:
    @allure.title("GET /accounts/contacts/download returns CSV")
    @pytest.mark.smoke
    def test_contacts_download_csv_contains_created_contact(self, created_contact):
        response, model = ContactsDownloadCsvAPI().download_contacts_csv(app_id=created_contact["app_id"])

        assert response.status_code == HTTPStatus.OK
        assert model.body_text.strip(), "CSV response is empty"
        assert ";" in model.body_text.splitlines()[0], "CSV header is not ';' separated"

        row = next(
            (line for line in model.body_text.splitlines() if created_contact["create_payload"]["Email"] in line),
            None,
        )
        assert row is not None, "Created contact email was not found in CSV export"
        assert created_contact["create_payload"]["FirstName"] in row
        assert created_contact["create_payload"]["LastName"] in row

    @allure.title("GET /accounts/contacts/{contact_id}/download returns VCF")
    @pytest.mark.smoke
    def test_contact_download_by_id_returns_vcard(self, created_contact):
        response, model = ContactDownloadByIdAPI().download_contact(
            created_contact["contact_id"],
            app_id=created_contact["app_id"],
        )

        assert response.status_code == HTTPStatus.OK
        assert model.is_vcard, "Expected VCF content"
        assert created_contact["create_payload"]["Email"] in model.body_text
