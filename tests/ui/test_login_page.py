import pytest
from playwright.sync_api import Page

from tests.ui.login_page import LoginPage

pytestmark = pytest.mark.ui  # 标记整个模块为 UI 测试

@pytest.mark.smoke
def test_user_can_login_and_see_products(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)

    login_page.open()
    login_page.login("admin", "password123")
    login_page.expect_login_success()

    
       


def test_user_sees_error_with_wrong_password(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)

    login_page.open()
    login_page.login("admin", "wrong-password")
    login_page.expect_login_failed()



