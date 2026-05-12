from playwright.sync_api import Page, expect, sync_playwright


def test_user_can_login_and_see_products(base_url: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()

        page.goto(base_url)
        page.get_by_label("用户名").fill("admin")
        page.get_by_label("密码").fill("password123")
        page.get_by_role("button", name="登录").click()

        expect(page.get_by_text("登录成功")).to_be_visible()
        expect(page.get_by_role("heading", name="商品列表")).to_be_visible()
        expect(page.get_by_text("接口测试入门课")).to_be_visible()

        browser.close()


def test_user_sees_error_with_wrong_password(base_url: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page: Page = browser.new_page()

        page.goto(base_url)
        page.get_by_label("用户名").fill("admin")
        page.get_by_label("密码").fill("wrong-password")
        page.get_by_role("button", name="登录").click()

        expect(page.get_by_text("用户名或密码错误")).to_be_visible()
        expect(page.get_by_role("heading", name="商品列表")).not_to_be_visible()

        browser.close()

