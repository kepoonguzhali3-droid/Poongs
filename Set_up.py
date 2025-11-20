# ---------- IMPORTS ----------
import pytest
from playwright.sync_api import sync_playwright

# ---------- PAGE OBJECT ----------
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.email = "input[type='email']"
        self.next_btn = "#identifierNext"
        self.pass_input = "input[type='password']"
        self.pass_next_btn = "#passwordNext"
        self.pass_next_btn = "#passwordNext"

    def login(self, email, password):
        self.page.goto("https://gmail.com")
        self.page.fill(self.email, email)
        self.page.click(self.next_btn)
        self.page.wait_for_selector(self.pass_input)
        self.page.fill(self.pass_input, password)
        self.page.click(self.pass_next_btn)
        self.page.wait_for_load_state("networkidle")


# ---------- TEST DATA ----------
def get_login_data():
    return {
        "Email": "testuser@gmail.com",
        "Password": "Test@123"
    }


# ---------- FIXTURE (Browser + Login + Return Page) ----------
@pytest.fixture()
def logged_in_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # login
        data = get_login_data()
        LoginPage(page).login(data["Email"], data["Password"])

        yield page

        context.close()
        browser.close()


# ---------- TEST ----------
def test_inbox_navigation(logged_in_page):
    page = logged_in_page
    assert "inbox" in page.url.lower()
    print("Login successful & inbox opened!")
