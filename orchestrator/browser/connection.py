from playwright.async_api import Browser, Playwright
from orchestrator.config import DEFAULT_CDP_URL


async def connect_browser(playwright_instance: Playwright, cdp_url: str = DEFAULT_CDP_URL) -> Browser:
    """Connect to a running Chrome session using the Chrome DevTools Protocol (CDP)."""
    try:
        return await playwright_instance.chromium.connect_over_cdp(cdp_url)
    except Exception as e:
        print(f"\n[!] Could not connect to Chrome over CDP at {cdp_url}.")
        print("Run: python start_browser.py (or ./start_browser.sh on macOS/Linux)")
        raise e
