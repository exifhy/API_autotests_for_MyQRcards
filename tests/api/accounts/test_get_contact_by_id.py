import allure
import pytest

from services.accounts.accounts_contact_by_id.api_accounts_contact_by_id import (
    AccountsContactByIdAPI,
)


@allure.epic("API")
@allure.feature("Accounts")
@allure.title("GET /accounts/contacts/{contactID}")
@pytest.mark.api
@pytest.mark.accounts
@pytest.mark.smoke
@allure.description(
    """
    /accounts/contacts/{contactID}
    """
)
def test_get_contact_by_id_200(cfg):
    contact_id = cfg.get("lk_contact_id")
    assert contact_id, "cfg['lk_contact_id'] is empty. Add lk_contact_id to ids.<env>.json"

    model = AccountsContactByIdAPI().get_contact_by_id(contact_id)

    assert model.contactID == int(contact_id)
    assert any([model.firstName, model.lastName, model.email, model.mobilePhone])
