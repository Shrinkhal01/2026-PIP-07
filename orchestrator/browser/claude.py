import asyncio
from playwright.async_api import async_playwright
from orchestrator.config import DEFAULT_CDP_URL
from orchestrator.browser.connection import connect_browser


async def run_claude_prompt(prompt_text: str, cdp_url: str = DEFAULT_CDP_URL) -> str:
    """Send a prompt to an authenticated Claude tab, wait for response, and return scraped text."""
    async with async_playwright() as p:
        print("Connecting to your running Chrome session...")
        browser = await connect_browser(p, cdp_url=cdp_url)
        context = browser.contexts[0]
        page = await context.new_page()

        try:
            print("Navigating to Claude...")
            for attempt in range(3):
                try:
                    await page.goto("https://claude.ai/new", wait_until="domcontentloaded")
                    break
                except Exception as e:
                    if attempt == 2:
                        raise e
                    await asyncio.sleep(2)

            print("Sending prompt to Claude...")
            textarea = page.locator("div.tiptap.ProseMirror[contenteditable='true'], div[contenteditable='true'], textarea").first
            await textarea.wait_for(state="visible", timeout=30000)
            await textarea.fill(prompt_text)

            # Click send button or press Enter
            try:
                send_btn = page.locator("button[aria-label='Send message'], button[data-testid='chat-input-send']").first
                if await send_btn.is_visible(timeout=2000):
                    await send_btn.click()
                else:
                    await textarea.press("Enter")
            except Exception:
                await textarea.press("Enter")

            print("Waiting for Claude response...")
            # Wait for generation to start / stop button
            try:
                await page.wait_for_selector(
                    "button[aria-label*='Stop'], [data-is-streaming='true']",
                    timeout=8000
                )
                print("Generation in progress...")
                await page.wait_for_selector(
                    "button[aria-label*='Stop'], [data-is-streaming='true']",
                    state="detached",
                    timeout=180000
                )
            except Exception:
                print("Monitoring response stream...")
                last_len = 0
                stable_count = 0
                for _ in range(60):
                    await asyncio.sleep(2)
                    text = await page.evaluate("""() => {
                        const msgs = document.querySelectorAll(".font-claude-response, .font-claude-message, .standard-markdown");
                        return msgs.length > 0 ? msgs[msgs.length - 1].innerText.length : 0;
                    }""")
                    if text > 0 and text == last_len:
                        stable_count += 1
                        if stable_count >= 3:
                            break
                    else:
                        stable_count = 0
                        last_len = text

            await asyncio.sleep(2)

            # Scrape response text
            responses = await page.query_selector_all(".font-claude-response, .font-claude-message, .standard-markdown")
            last_response = await responses[-1].inner_text() if responses else "Error reading Claude output."

            return last_response.strip()

        finally:
            await page.close()
