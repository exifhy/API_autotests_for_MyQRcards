import allure
import pytest
from http import HTTPStatus

from services.subscriptions.subscription_invitation_create.api_subscription_invitation_create import (
    SubscriptionInvitationCreateAPI,
)
from services.subscriptions.subscription_invitation_delete.api_subscription_invitation_delete import (
    SubscriptionInvitationDeleteAPI,
)
from services.subscriptions.subscription_moderator_get.api_subscription_moderator_get import (
    SubscriptionModeratorGetAPI,
)
from services.subscriptions.subscription_moderators_add.api_subscription_moderators_add import (
    SubscriptionModeratorsAddAPI,
)
from services.subscriptions.subscription_moderators_delete.api_subscription_moderators_delete import (
    SubscriptionModeratorsDeleteAPI,
)
from services.subscriptions.subscription_moderators_list.api_subscription_moderators_list import (
    SubscriptionModeratorsListAPI,
)


@allure.epic("API")
@allure.feature("Subscriptions")
@pytest.mark.api
@allure.description(
    """
    620 GET  /subscriptions/{id}/moderators
    621 POST /subscriptions/{id}/moderators
    622 DELETE /subscriptions/{id}/moderators
    623 GET  /subscriptions/{id}/moderators/{accountId}
    """
)
class TestSubscriptionModerators:
    @allure.title("620 GET /subscriptions/{id}/moderators -> 200/204")
    def test_subscription_moderators_list_200(self, cfg):
        sub_id = int(cfg["subscription_id"])

        response, model = SubscriptionModeratorsListAPI().get_subscription_moderators(sub_id)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
        assert isinstance(model.items, list)

    @allure.title(
        "621+622+623: POST invitation -> POST moderator -> GET list -> GET by id -> DELETE moderator -> DELETE invitation"
    )
    def test_subscription_moderator_add_get_delete_flow(self, cfg):
        sub_id = int(cfg["subscription_id"])
        company_id = int(cfg["company_id_create"])
        invite_id = None

        try:
            with allure.step(f"POST /Subscriptions/{sub_id}/invitation"):
                _, created, _ = SubscriptionInvitationCreateAPI().create_subscription_invitation(
                    sub_id,
                    company_id=company_id,
                )
                assert created.id is not None, "Invitation id is empty"
                invite_id = int(created.id)
                account_id = invite_id

            with allure.step(f"621 POST /subscriptions/{sub_id}/moderators (account_id={account_id})"):
                add_response = SubscriptionModeratorsAddAPI().add_subscription_moderator(sub_id, account_id)
                assert add_response.status_code in (
                    HTTPStatus.OK,
                    HTTPStatus.CREATED,
                    HTTPStatus.ACCEPTED,
                    HTTPStatus.NO_CONTENT,
                    HTTPStatus.CONFLICT,
                )

            with allure.step(f"620 GET /subscriptions/{sub_id}/moderators — verify account_id present"):
                _, mod_list = SubscriptionModeratorsListAPI().get_subscription_moderators(sub_id)
                assert isinstance(mod_list.items, list)
                account_ids = [item.accountID for item in mod_list.items]
                assert account_id in account_ids, (
                    f"account_id={account_id} not found in moderators list: {account_ids}"
                )

            with allure.step(f"623 GET /subscriptions/{sub_id}/moderators/{account_id}"):
                moderator = SubscriptionModeratorGetAPI().get_subscription_moderator(sub_id, account_id)
                assert int(moderator.accountID) == account_id

            with allure.step(f"622 DELETE /subscriptions/{sub_id}/moderators (account_id={account_id})"):
                del_response = SubscriptionModeratorsDeleteAPI().delete_subscription_moderator(sub_id, account_id)
                assert del_response.status_code in (
                    HTTPStatus.OK,
                    HTTPStatus.ACCEPTED,
                    HTTPStatus.NO_CONTENT,
                    HTTPStatus.NOT_FOUND,
                    HTTPStatus.CONFLICT,
                )

        finally:
            if invite_id:
                try:
                    SubscriptionInvitationDeleteAPI().delete_subscription_invitation(sub_id, invite_id)
                except Exception:
                    pass
