import allure
import pytest

from services.promotions.promotion_by_id.api_promotion_by_id import PromotionByIdAPI


@allure.epic("API")
@allure.feature("Promotions")
@pytest.mark.api
@allure.description(
    """
    /promotions/{id}
    """
)
class TestPromotionById:
    @allure.title("GET /promotions/{id} returns promotion")
    @pytest.mark.smoke
    @pytest.mark.skip(reason="hardcoded promotion ID exists only on dev")
    def test_promotion_by_id_200(self):
        promotion_id = "ErfD4RtfDDTvvEDdErfD4RtfDDTvvEDd"

        model = PromotionByIdAPI().get_promotion_by_id(promotion_id)

        assert model.id == promotion_id
        assert model.title is None or model.title != ""
        assert model.message is None or model.message != ""

