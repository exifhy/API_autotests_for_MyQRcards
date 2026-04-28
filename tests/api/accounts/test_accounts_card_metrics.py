import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_card_metrics_delete.api_accounts_card_metrics_delete import (
    AccountsCardMetricsDeleteAPI,
)
from services.accounts.accounts_card_metrics.api_accounts_card_metrics import AccountsCardMetricsAPI
from services.accounts.accounts_card_metrics_update.api_accounts_card_metrics_update import (
    AccountsCardMetricsUpdateAPI,
)
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.card_metrics_update.api_card_metrics_update import CardMetricsUpdateAPI
from services.metrics.metric_types.api_metric_types import MetricTypesAPI


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    /Accounts/{accountID}/Cards/{cardID}/metrics
    """
)
class TestAccountsCardMetrics:
    @allure.title("POST /Cards -> PUT /Cards/{id}/metrics -> GET /Accounts/{accountID}/Cards/{cardID}/metrics")
    @pytest.mark.smoke
    def test_accounts_card_metrics_after_update_flow(self, created_card):
        created = created_card

        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        _, metric_types = MetricTypesAPI().get_metric_types(offset=0, fetch=10)
        assert metric_types.items, "MetricTypes list is empty"
        metric_type_id = next((item.id for item in metric_types.items if item.id is not None), None)
        assert metric_type_id is not None, "No metricTypeID found in /MetricTypes"

        updated = CardMetricsUpdateAPI().update_card_metrics(created.id, metric_type_id=metric_type_id)
        assert updated.status_code == HTTPStatus.ACCEPTED

        response, model = AccountsCardMetricsAPI().get_accounts_card_metrics(
            card.accountID,
            created.id,
            range_header="items=0-49",
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        assert model.items, "Expected non-empty metrics list after PUT /Cards/{id}/metrics"
        assert any(item.cardID == created.id for item in model.items if item.cardID is not None)
        assert any(item.accountID == card.accountID for item in model.items if item.accountID is not None)

    @allure.title("POST /Cards -> PUT /Accounts/{accountID}/Cards/{cardID}/metrics -> GET /Accounts/{accountID}/Cards/{cardID}/metrics")
    def test_accounts_card_metrics_merge_flow(self, created_card):
        created = created_card

        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        _, metric_types = MetricTypesAPI().get_metric_types(offset=0, fetch=10)
        assert metric_types.items, "MetricTypes list is empty"
        metric_type_id = next((item.id for item in metric_types.items if item.id is not None), None)
        assert metric_type_id is not None, "No metricTypeID found in /MetricTypes"

        updated, _ = AccountsCardMetricsUpdateAPI().update_accounts_card_metrics(
            card.accountID,
            created.id,
            metric_type_id=metric_type_id,
        )
        assert updated.status_code == HTTPStatus.ACCEPTED

        response, model = AccountsCardMetricsAPI().get_accounts_card_metrics(card.accountID, created.id)
        assert response.status_code == HTTPStatus.OK
        assert model.items, "Expected non-empty metrics list after PUT /Accounts/{accountID}/Cards/{cardID}/metrics"
        assert any(item.metricTypeID == metric_type_id for item in model.items if item.metricTypeID is not None)

    @allure.title("GET /Accounts/{accountID}/Cards/{cardID}/metrics supports offset/fetch query")
    def test_accounts_card_metrics_with_paging_query(self, created_card):
        created = created_card

        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        response, model = AccountsCardMetricsAPI().get_accounts_card_metrics(
            card.accountID,
            created.id,
            offset=0,
            fetch=10,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT, HTTPStatus.PARTIAL_CONTENT)
        assert isinstance(model.items, list)

    @allure.title("GET /Accounts/{accountID}/Cards/{cardID}/metrics without auth")
    @pytest.mark.ng
    def test_accounts_card_metrics_without_auth(self, created_card):
        created = created_card

        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        response = AccountsCardMetricsAPI().get_accounts_card_metrics_without_auth(card.accountID, created.id)
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)

    @allure.title("POST /Cards -> PUT /Accounts/{accountID}/Cards/{cardID}/metrics -> DELETE /Accounts/{accountID}/Cards/{cardID}/metrics")
    def test_accounts_card_metrics_delete_flow(self, created_card):
        created = created_card

        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        _, metric_types = MetricTypesAPI().get_metric_types(offset=0, fetch=10)
        assert metric_types.items, "MetricTypes list is empty"
        metric_type_id = next((item.id for item in metric_types.items if item.id is not None), None)
        assert metric_type_id is not None, "No metricTypeID found in /MetricTypes"

        updated, _ = AccountsCardMetricsUpdateAPI().update_accounts_card_metrics(
            card.accountID,
            created.id,
            metric_type_id=metric_type_id,
        )
        assert updated.status_code == HTTPStatus.ACCEPTED

        deleted = AccountsCardMetricsDeleteAPI().delete_accounts_card_metrics(
            card.accountID,
            created.id,
            [metric_type_id],
        )
        assert deleted.status_code == HTTPStatus.ACCEPTED

        response, model = AccountsCardMetricsAPI().get_accounts_card_metrics(card.accountID, created.id)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
        assert all(item.metricTypeID != metric_type_id for item in model.items if item.metricTypeID is not None)

