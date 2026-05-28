import allure
import pytest
from http import HTTPStatus

from services.contacts.contacts_list.api_contacts_list import ContactsListAPI


@allure.epic("LK")
@allure.feature("Contacts")
@allure.title("Contact list")
@pytest.mark.contacts
@pytest.mark.e2e
class TestContactList:
    @allure.title("Accounts contact list returns 200 and list")
    def test_contact_list_returns_200(self, cfg):
        response, items = ContactsListAPI().get_contacts(app_id=str(cfg.get("x_application_id") or "3"))

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Expected HTTPStatus.OK/HTTPStatus.PARTIAL_CONTENT, got {response.status_code}, body={response.text}"
        )
        assert isinstance(items, list), f"Expected list in response, got: {type(items)}"
