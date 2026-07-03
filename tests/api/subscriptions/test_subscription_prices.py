import allure
import pytest
from http import HTTPStatus

from services.subscriptions.subscription_prices.api_subscription_prices import SubscriptionPricesAPI


@allure.epic("API")
@allure.feature("Subscriptions")
@pytest.mark.api
@allure.description(
    """
    GET /SubscriptionPrices
    613 — цены подписок с типом, валютой, ценой без скидки, ценой со скидкой и размером скидки.
    """
)
class TestSubscriptionPrices:
    @allure.title("GET /SubscriptionPrices — returns list with price fields")
    @pytest.mark.smoke
    def test_subscription_prices_200(self):
        model = SubscriptionPricesAPI().get_subscription_prices()

        assert isinstance(model.items, list), "Expected list of prices"
        assert model.items, "Expected non-empty prices list"

        for item in model.items:
            assert item.subscriptionType is not None, "subscriptionType is missing"
            assert item.currencyCode, "currencyCode is empty"
            assert item.price is not None, "price is missing"
            assert item.discountedPrice is not None, "discountedPrice is missing"
            assert item.discountPercent is not None, "discountPercent is missing"

    @allure.title("GET /SubscriptionPrices — discount consistency: discountedPrice <= price")
    def test_subscription_prices_discount_consistency(self):
        model = SubscriptionPricesAPI().get_subscription_prices()

        for item in model.items:
            if item.discountPercent and item.discountPercent > 0:
                assert item.discountedPrice < item.price, (
                    f"discountedPrice ({item.discountedPrice}) must be < price ({item.price}) "
                    f"when discountPercent={item.discountPercent}"
                )
            else:
                assert item.discountedPrice == item.price or item.discountedPrice is None, (
                    f"When no discount, discountedPrice ({item.discountedPrice}) "
                    f"should equal price ({item.price})"
                )

    @allure.title("GET /SubscriptionPrices — public endpoint, no auth required")
    @pytest.mark.ng
    def test_subscription_prices_public_no_auth(self):
        response = SubscriptionPricesAPI().get_subscription_prices_without_auth()
        assert response.status_code == HTTPStatus.OK, (
            f"Expected 200 (public endpoint), got {response.status_code}: {response.text}"
        )
