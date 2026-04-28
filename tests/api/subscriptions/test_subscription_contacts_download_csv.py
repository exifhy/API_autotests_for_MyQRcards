import allure
import pytest
from http import HTTPStatus

from services.subscriptions.subscription_contacts_download_csv.api_subscription_contacts_download_csv import (
    SubscriptionContactsDownloadCsvAPI,
)


@allure.epic("API")
@allure.feature("Subscriptions")
@pytest.mark.api
@allure.description(
    """
    /Subscriptions/{subscription_id}/contacts/download
    """
)
class TestSubscriptionContactsDownloadCsv:
    @allure.title("GET /Subscriptions/{subscription_id}/contacts/download returns CSV")
    def test_subscription_contacts_download_csv_200(self, cfg):
        sub_id = cfg.get("subscription_id")
        assert sub_id, "cfg['subscription_id'] is empty"

        date_from = "2025-01-01T00:00:00"
        date_till = SubscriptionContactsDownloadCsvAPI.current_date_till()

        response, model = SubscriptionContactsDownloadCsvAPI().download_subscription_contacts_csv(
            int(sub_id),
            date_from=date_from,
            date_till=date_till,
        )

        assert response.status_code == HTTPStatus.OK
        assert model.body_text.strip(), "CSV response is empty"
        assert "," in model.body_text or ";" in model.body_text, "CSV content does not look like CSV"

    @allure.title("GET /Subscriptions/{subscription_id}/contacts/download without auth")
    @pytest.mark.ng
    def test_subscription_contacts_download_csv_401_without_auth(self, cfg):
        sub_id = cfg.get("subscription_id")
        assert sub_id, "cfg['subscription_id'] is empty"

        date_from = "2025-01-01T00:00:00"
        date_till = SubscriptionContactsDownloadCsvAPI.current_date_till()

        response = SubscriptionContactsDownloadCsvAPI().download_subscription_contacts_csv_without_auth(
            int(sub_id),
            date_from=date_from,
            date_till=date_till,
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
