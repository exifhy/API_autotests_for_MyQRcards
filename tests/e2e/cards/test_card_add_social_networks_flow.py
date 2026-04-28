import allure
import pytest
from http import HTTPStatus

from services.cards.card_delete_by_id.api_card_delete_by_id import CardDeleteByIdAPI
from src.resources.api import merge_card_attributes
from tests.e2e.cards.helpers import (
    build_card_attributes_socials_body,
    create_card_and_fill_flow,
    wait_card_socials_in_0852,
)


@allure.epic("LK")
@allure.feature("Cards")
@allure.title("Create card -> Add all social networks -> Verify via 085 -> Delete")
@allure.description(
    """
    /Cards
    /accounts/{accountID}/cards/{cardID}/attributes
    /accounts/{accountID}/cards/{cardID}/attributes/
    /Cards/{id}
    """
)
@pytest.mark.e2e
class TestCardAddSocialNetworksFlow:
    @allure.title("Create card")
    def test_01_create_card(self, cfg, card_leadgen_flow):
        create_card_and_fill_flow(
            card_leadgen_flow,
            subscription_id=cfg["subscription_id"],
            company_id=cfg["company_id_create"],
        )
        assert card_leadgen_flow["card_id"], "card_id empty after create"
        assert card_leadgen_flow["account_id"], "account_id empty after create"

    @allure.title("Merge all social networks into card attributes")
    def test_02_add_all_social_networks(self, lk_api, card_leadgen_flow, social_attributes_11_37):
        card_id = card_leadgen_flow["card_id"]
        account_id = card_leadgen_flow["account_id"]
        assert card_id, "card_id empty (test_01 failed?)"
        assert account_id, "account_id empty (test_01 failed?)"

        body, expected_urls = build_card_attributes_socials_body(social_attributes_11_37)
        card_leadgen_flow["social_payload"] = body
        card_leadgen_flow["social_expected_urls"] = expected_urls

        response = merge_card_attributes(
            lk_api,
            account_id=int(account_id),
            card_id=int(card_id),
            body=body,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"CardAttribute/Merge socials failed: {response.status_code}, body={response.text}"
        )

    @allure.title("085 contains all social networks")
    def test_03_verify_socials_in_085(self, lk_api, card_leadgen_flow):
        card_id = card_leadgen_flow["card_id"]
        account_id = card_leadgen_flow["account_id"]
        expected_urls = card_leadgen_flow.get("social_expected_urls")
        assert card_id, "card_id empty (test_01 failed?)"
        assert account_id, "account_id empty (test_01 failed?)"
        assert expected_urls, "social_expected_urls empty (test_02 failed?)"

        items = wait_card_socials_in_0852(
            lk_api,
            account_id=account_id,
            card_id=card_id,
            expected_urls_by_name=expected_urls,
            timeout_s=90,
            step_s=3,
        )
        assert items is not None, "Not all social networks were found in 085 attributes list"

    @allure.title("Delete card")
    def test_04_delete_card(self, card_leadgen_flow):
        card_id = card_leadgen_flow["card_id"]
        assert card_id, "card_id empty (test_01 failed?)"

        response = CardDeleteByIdAPI().delete_card_by_id(card_id)
        assert response.status_code == HTTPStatus.ACCEPTED
        card_leadgen_flow["deleted"] = True
