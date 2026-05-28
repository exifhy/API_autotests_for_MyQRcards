from datetime import UTC, datetime, timedelta
from http import HTTPStatus

import allure
import pytest

from services.cardlinks.cardlinks_statistic.api_cardlinks_statistic import CardLinksStatisticAPI


@allure.epic("API")
@allure.feature("CardLinks")
@pytest.mark.api
@allure.description(
    """
    /cardlinks/statistic
    """
)
class TestCardLinksStatistic:
    @allure.title("GET /cardlinks/statistic returns list")
    @pytest.mark.smoke
    def test_cardlinks_statistic_flow(self):
        date_till = datetime.now(UTC)
        date_from = date_till - timedelta(days=7)

        response, model = CardLinksStatisticAPI().get_cardlinks_statistic(
            date_from=date_from.strftime("%Y-%m-%dT%H:%M:%S"),
            date_till=date_till.strftime("%Y-%m-%dT%H:%M:%S"),
        )

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
        assert isinstance(model.items, list)
