import allure
import pytest
from http import HTTPStatus

from services.metrics.metric_types.api_metric_types import MetricTypesAPI


@allure.epic("API")
@allure.feature("Metrics")
@pytest.mark.api
@allure.description(
    """
    /MetricTypes
    """
)
class TestMetricTypes:
    @allure.title("GET /MetricTypes returns metric types list")
    @pytest.mark.smoke
    def test_metric_types_200_or_206(self):
        response, model = MetricTypesAPI().get_metric_types(range_header="items=0-199")

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        if response.status_code == HTTPStatus.PARTIAL_CONTENT:
            content_range = response.headers.get("Content-Range") or response.headers.get("content-range")
            assert content_range, "Expected Content-Range header for 206 response"

        assert isinstance(model.items, list)
        assert model.items, "Metric types list is empty"
        assert model.items[0].id is not None
        assert model.items[0].name is None or model.items[0].name != ""

    @allure.title("GET /MetricTypes supports offset/fetch query")
    def test_metric_types_with_paging_query(self):
        response, model = MetricTypesAPI().get_metric_types(offset=0, fetch=50)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        assert isinstance(model.items, list)

    @allure.title("GET /MetricTypes without auth")
    @pytest.mark.ng
    def test_metric_types_401_without_auth(self):
        response = MetricTypesAPI().get_metric_types_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
