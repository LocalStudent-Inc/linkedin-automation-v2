import json
from playwright.sync_api import sync_playwright

with open("credentials.json") as f:
    credentials = json.load(f)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.linkedin.com/")

        login_button = page.locator('a[data-tracking-control-name="guest_homepage-basic_nav-header-signin"]')
        login_button.click()

        email_field = page.locator('input[name="session_key"]')
        email_field.fill(credentials["username"])

        password_field = page.locator('input[name="session_password"]')
        password_field.fill(credentials["password"])

        submit_button = page.locator('button[type="submit"]')
        submit_button.click()
        page.wait_for_load_state()

        search_field = page.locator('input[placeholder="Search"]')
        search_field.fill("marco tan localstudent")
        page.keyboard.press("Enter")

        profile_link = page.locator('a[href="/in/marcotan04"]')
        profile_link.click()
        page.wait_for_load_state()

        page.screenshot(path="screenshot.png")
        browser.close()

if __name__ == "__main__":
    main()
