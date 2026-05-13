from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url

    def open(self) -> None:
        self.page.goto(self.base_url)

    def login(self, username: str, password: str) -> None:
        self.page.get_by_label("用户名").fill(username)
        self.page.get_by_label("密码").fill(password)
        self.page.get_by_role("button", name="登录").click()

    def expect_login_success(self) -> None:
        expect(self.page.get_by_text("登录成功")).to_be_visible()
        expect(self.page.get_by_role("heading", name="商品列表")).to_be_visible()

    def expect_login_failed(self) -> None:
        expect(self.page.get_by_text("用户名或密码错误")).to_be_visible()
        expect(self.page.get_by_role("heading", name="商品列表")).not_to_be_visible()
