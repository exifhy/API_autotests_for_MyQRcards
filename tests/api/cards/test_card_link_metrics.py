import allure
import pytest
from http import HTTPStatus

from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.card_link_metrics.api_card_link_metrics import CardLinkMetricsAPI
from services.cards.card_metrics_update.api_card_metrics_update import CardMetricsUpdateAPI
from services.metrics.metric_types.api_metric_types import MetricTypesAPI
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/{id}/cardLink/metrics
    """
)
class TestCardLinkMetrics:
    @allure.title("POST /Cards -> PUT metrics -> GET /Cards/{cardLinkId}/cardLink/metrics -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_card_link_metrics_flow(self, created_card):
        created = created_card

        _, metric_types = MetricTypesAPI().get_metric_types(offset=0, fetch=10)
        metric_type_id = next((item.id for item in metric_types.items if item.id is not None), None)
        assert metric_type_id is not None, "No metricTypeID found in /MetricTypes"

        updated = CardMetricsUpdateAPI().update_card_metrics(created.id, metric_type_id=metric_type_id)
        assert updated.status_code == HTTPStatus.ACCEPTED

        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.url, "Card public url is empty"
        card_link_id = extract_card_link_id(card.url)

        response, model = CardLinkMetricsAPI().get_card_link_metrics(card_link_id, range_header="items=0-49")
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        assert model.items, "Expected non-empty metrics list for card link"
        assert any(item.cardID == created.id for item in model.items if item.cardID is not None)


    @allure.title("GET /Cards/{cardLinkId}/cardLink/metrics supports offset/fetch query")
    def test_card_link_metrics_with_paging_query(self, created_card):
        created = created_card

        _, metric_types = MetricTypesAPI().get_metric_types(offset=0, fetch=10)
        metric_type_id = next((item.id for item in metric_types.items if item.id is not None), None)
        assert metric_type_id is not None, "No metricTypeID found in /MetricTypes"

        updated = CardMetricsUpdateAPI().update_card_metrics(created.id, metric_type_id=metric_type_id)
        assert updated.status_code == HTTPStatus.ACCEPTED

        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.url, "Card public url is empty"
        card_link_id = extract_card_link_id(card.url)

        response, model = CardLinkMetricsAPI().get_card_link_metrics(
            card_link_id,
            offset=0,
            fetch=10,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        assert model.items, "Expected non-empty metrics list for card link"

