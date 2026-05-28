import pytest

from services.subscriptions.subscription_invitation_delete.api_subscription_invitation_delete import (
    SubscriptionInvitationDeleteAPI,
)


@pytest.fixture(scope="module")
def subscription_invitation_flow(cfg):
    state = {
        "subscription_id": cfg.get("subscription_id"),
        "company_id": cfg.get("company_id_create"),
        "invite_id": None,
        "payload": None,
        "deleted": False,
    }
    yield state

    invite_id = state.get("invite_id")
    sub_id = state.get("subscription_id")
    if invite_id and sub_id and not state.get("deleted"):
        try:
            SubscriptionInvitationDeleteAPI().delete_subscription_invitation(int(sub_id), int(invite_id))
        except Exception:
            pass
