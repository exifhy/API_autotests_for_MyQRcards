import allure
import pytest
from http import HTTPStatus

from services.cards.card_metrics.api_card_metrics import CardMetricsAPI
from services.cards.card_metrics_update.api_card_metrics_update import CardMetricsUpdateAPI
from services.metrics.metric_types.api_metric_types import MetricTypesAPI


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/{cardID}/metrics
    """
)
class TestCardMetrics:
    @allure.title("POST /Cards -> GET /Cards/{id}/metrics -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_card_metrics_flow(self, created_card):
        created = created_card

        response, model = CardMetricsAPI().get_card_metrics(created.id, range_header="items=0-49")
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT, HTTPStatus.PARTIAL_CONTENT)
        assert isinstance(model.items, list)
        if model.items:
            assert all(item.cardID in (None, created.id) for item in model.items)


    @allure.title("POST /Cards -> PUT metrics -> GET /Cards/{id}/metrics returns 200 -> DELETE /Cards/{id}")
    def test_card_metrics_after_update_flow(self, created_card):
        created = created_card

        _, metric_types = MetricTypesAPI().get_metric_types(offset=0, fetch=10)
        assert metric_types.items, "MetricTypes list is empty"
        metric_type_id = next((item.id for item in metric_types.items if item.id is not None), None)
        assert metric_type_id is not None, "No metricTypeID found in /MetricTypes"

        updated = CardMetricsUpdateAPI().update_card_metrics(created.id, metric_type_id=metric_type_id)
        assert updated.status_code == HTTPStatus.ACCEPTED

        response, model = CardMetricsAPI().get_card_metrics(created.id)
        assert response.status_code == HTTPStatus.OK
        assert model.items, "Expected non-empty metrics list after PUT /Cards/{id}/metrics"
        assert any(item.cardID == created.id for item in model.items if item.cardID is not None)


    @allure.title("GET /Cards/{id}/metrics supports offset/fetch query")
    def test_card_metrics_with_paging_query(self, created_card):
        created = created_card

        response, model = CardMetricsAPI().get_card_metrics(
            created.id,
            offset=0,
            fetch=10,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT, HTTPStatus.PARTIAL_CONTENT)
        assert isinstance(model.items, list)


    @allure.title("GET /Cards/{id}/metrics without auth")
    @pytest.mark.ng
    def test_card_metrics_401_without_auth(self, created_card):
        created = created_card

        response = CardMetricsAPI().get_card_metrics_without_auth(created.id)
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)

