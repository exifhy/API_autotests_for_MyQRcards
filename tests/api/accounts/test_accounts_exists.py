import allure
import pytest

from services.accounts.accounts_exists.api_accounts_exists import AccountsExistsAPI


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    /accounts/Exists
    """
)
class TestAccountsExists:
    @allure.title("Exists returns true for known email")
    @pytest.mark.smoke
    def test_accounts_exists_true_for_known_email(self, cfg):
        email = cfg.get("lk_email")
        assert email, "cfg['lk_email'] is empty"

        model = AccountsExistsAPI().get_exists(email)

        assert isinstance(model.exists, bool)
        assert model.exists is True, f"Expected true for email={email}, got {model.exists}"

    @allure.title("Exists returns false for random email")
    @pytest.mark.ng
    def test_accounts_exists_false_for_random_email(self):
        email = "autotest_no_such_user_1234567890@example.com"

        model = AccountsExistsAPI().get_exists(email)

        assert isinstance(model.exists, bool)
        assert model.exists is False, (
            f"Expected false for random email={email}, got {model.exists}"
        )
