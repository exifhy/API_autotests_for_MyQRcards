import allure
import pytest
from http import HTTPStatus

from services.subscriptions.subscription_invitation_create.api_subscription_invitation_create import (
    SubscriptionInvitationCreateAPI,
)
from services.subscriptions.subscription_invitation_delete.api_subscription_invitation_delete import (
    SubscriptionInvitationDeleteAPI,
)
from tests.api.subscriptions.helpers import (
    wait_subscription_invitation_account_absent,
    wait_subscription_invitation_account_present,
)


@allure.epic("API")
@allure.feature("Subscriptions")
@pytest.mark.api
@allure.description(
    """
    /Subscriptions/{subscription_id}/invitation
    /accounts
    /Subscriptions/{subscription_id}/invitation/{invite_id}
    /accounts
    """
)
class TestSubscriptionInvitationFlow:
    @allure.title("POST invitation -> GET /accounts -> DELETE invitation -> GET /accounts")
    def test_subscription_invitation_crud_flow(self, subscription_invitation_flow):
        sub_id = subscription_invitation_flow.get("subscription_id")
        company_id = subscription_invitation_flow.get("company_id")
        assert sub_id, "cfg['subscription_id'] is empty"
        assert company_id, "cfg['company_id_create'] is empty"

        _, created, payload = SubscriptionInvitationCreateAPI().create_subscription_invitation(
            int(sub_id),
            company_id=int(company_id),
        )
        assert created.id is not None, "Invitation id is empty"
        subscription_invitation_flow["invite_id"] = int(created.id)
        subscription_invitation_flow["payload"] = payload

        found = wait_subscription_invitation_account_present(
            invite_id=int(created.id),
            expected_email=payload["Email"],
            timeout_s=60,
            step_s=3,
        )
        assert found is not None, "Created invitation/account not found in /accounts"
        assert int(found["id"]) == int(created.id)
        assert str(found.get("email") or "").strip().lower() == str(payload["Email"]).strip().lower()

        response = SubscriptionInvitationDeleteAPI().delete_subscription_invitation(int(sub_id), int(created.id))
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND)
        subscription_invitation_flow["deleted"] = True

        is_absent = wait_subscription_invitation_account_absent(
            invite_id=int(created.id),
            timeout_s=60,
            step_s=3,
        )
        assert is_absent is True, "Invitation/account is still present in /accounts after delete"
