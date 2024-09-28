import re
from playwright.sync_api import (Playwright, sync_playwright, expect)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page.get_by_label("Search", exact=True).click()
    page.get_by_label("Search", exact=True).fill("rohit bhardwaj")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
