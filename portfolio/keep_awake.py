import re
from playwright.sync_api import sync_playwright

URLS = [
    "https://mahmoud-data-cleaner.streamlit.app",
    "https://mahmoud-web-scraper.streamlit.app",
    "https://mahmoud-multi-scraper.streamlit.app",
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for url in URLS:
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        try:
            page.get_by_role(
                "button", name=re.compile("get this app back up", re.I)
            ).click(timeout=8000)
            print(f"{url}: was asleep, woke it")
        except Exception:
            print(f"{url}: already awake")
        page.wait_for_timeout(30000)  # stay long enough to connect
        page.close()
    browser.close()