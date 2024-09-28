import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page.get_by_label("Search", exact=True).click()
    page.get_by_label("Search", exact=True).fill("hikvision nvr")
    page.goto("https://www.google.com/search?q=hikvision+nvr&sca_esv=12fe31487ad231eb&source=hp&ei=NiMZZuGPHpi-vr0Pu7-OoAk&iflsig=ANes7DEAAAAAZhkxRgkYIsi9BNgwGEgOtntI5yG2OZd4&ved=0ahUKEwjhgrmM0byFAxUYn68BHbufA5QQ4dUDCA0&uact=5&oq=hikvision+nvr&gs_lp=Egdnd3Mtd2l6Ig1oaWt2aXNpb24gbnZyMggQABiABBixAzIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABEjGN1DjDViZJ3ABeACQAQCYAXigAfUKqgEEMS4xMrgBA8gBAPgBAZgCDqACrguoAgrCAhAQABgDGI8BGOUCGOoCGIwDwgILEAAYgAQYsQMYgwHCAhEQLhiDARjHARixAxjRAxiABMICCxAuGIAEGLEDGIMBwgIOEC4YgAQYigUYsQMYgwHCAggQLhiABBixA8ICDhAAGIAEGIoFGLEDGIMBwgIOEC4YgAQYsQMYxwEY0QPCAgsQLhiDARixAxiABMICDhAuGMcBGLEDGNEDGIAEmAMHkgcEMS4xM6AHs2I&sclient=gws-wiz")
    page.get_by_role("button", name="Search", exact=True).click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
