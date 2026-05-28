import allure
import pytest
from http import HTTPStatus

from services.contacts.contact_create_app.api_contact_create_app import ContactCreateAppAPI
from services.contacts.contacts_download_csv.api_contacts_download_csv import ContactsDownloadCsvAPI
from services.subscriptions.subscription_contacts_delete.api_subscription_contacts_delete import (
    SubscriptionContactsDeleteAPI,
)
from tests.e2e.contacts.helpers import wait_for_contact
from src.support.waiter import wait_until


@allure.epic("LK")
@allure.feature("Contacts")
@allure.title("Contact CSV export")
@pytest.mark.contacts
@pytest.mark.e2e
@pytest.mark.export
class TestContactDownloadCsv:
    @allure.title("Create contact returns id")
    def test_01_create_contact_returns_id(self, contact_csv_flow):
        model = ContactCreateAppAPI().create_contact(
            contact_csv_flow["payload"],
            app_id=contact_csv_flow["application_id"],
        )
        assert model.id, "No id in create response"
        contact_csv_flow["contact_id"] = int(model.id)

    @allure.title("Contact GET returns expected contact")
    def test_02_get_contact_returns_200(self, contact_csv_flow):
        contact_id = contact_csv_flow["contact_id"]
        assert contact_id, "contact_id empty (test_01 failed?)"

        found = wait_for_contact(
            contact_id,
            app_id=contact_csv_flow["application_id"],
            email=contact_csv_flow["payload"]["Email"],
            timeout_s=60,
            step_s=3,
        )
        assert found is not None, f"Contact GET did not return expected contact_id={contact_id}"

    @allure.title("CSV contains created contact")
    def test_03_download_contacts_csv_contains_contact(self, contact_csv_flow):
        assert contact_csv_flow["contact_id"], "contact_id empty (test_01 failed?)"

        def _csv():
            response, model = ContactsDownloadCsvAPI().download_contacts_csv(
                app_id=contact_csv_flow["application_id"],
            )
            if response.status_code != HTTPStatus.OK or not model.body_text:
                return None
            return model

        model = wait_until(_csv, timeout_s=90, step_s=5)
        assert model is not None, "CSV download failed or returned empty body"

        csv_text = model.body_text
        assert csv_text.strip(), "CSV response is empty"

        lines = csv_text.splitlines()
        assert lines, "CSV has no lines"
        header = lines[0]
        assert ";" in header, f"CSV header does not look ';' separated: {header}"

        email = contact_csv_flow["payload"]["Email"]
        first_name = contact_csv_flow["payload"]["FirstName"]
        last_name = contact_csv_flow["payload"]["LastName"]
        company_name = contact_csv_flow["payload"]["CompanyName"]
        position = contact_csv_flow["payload"]["Position"]

        row = next((line for line in lines[1:] if email in line), None)
        assert row is not None, f"Row with email not found in CSV: {email}"
        assert first_name in row, f"FirstName not found in CSV row: {row}"
        assert last_name in row, f"LastName not found in CSV row: {row}"
        assert company_name in row, f"CompanyName not found in CSV row: {row}"
        assert position in row, f"Position not found in CSV row: {row}"

    @allure.title("Delete contact")
    def test_04_delete_contact(self, contact_csv_flow):
        contact_id = contact_csv_flow["contact_id"]
        assert contact_id, "contact_id empty (test_01 failed?)"

        response = SubscriptionContactsDeleteAPI().delete_subscription_contacts(
            contact_csv_flow["subscription_id"],
            [contact_id],
            app_id=contact_csv_flow["application_id"],
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Delete contact failed: {response.status_code}, body={response.text}"
        )
        contact_csv_flow["deleted"] = True
