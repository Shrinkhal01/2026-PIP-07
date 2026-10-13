import asyncio
from playwright.async_api import async_playwright
from orchestrator.config import DEFAULT_CDP_URL
from orchestrator.browser.connection import connect_browser


async def run_chatgpt_prompt(prompt_text: str, cdp_url: str = DEFAULT_CDP_URL) -> str:
    """Send a prompt to an authenticated ChatGPT tab, wait for response, and return scraped text."""
    async with async_playwright() as p:
        print("Connecting to your running Chrome session...")
        browser = await connect_browser(p, cdp_url=cdp_url)
        context = browser.contexts[0]
        page = await context.new_page()

        try:
            print("Navigating to ChatGPT...")
            for attempt in range(3):
                try:
                    await page.goto("https://chatgpt.com", wait_until="domcontentloaded")
                    break
                except Exception as e:
                    if attempt == 2:
                        raise e
                    await asyncio.sleep(2)

            print("Sending prompt to ChatGPT...")
            textarea = page.locator("div.ProseMirror[contenteditable='true'], #prompt-textarea, textarea").first
            await textarea.wait_for(state="visible", timeout=30000)
            await textarea.fill(prompt_text)

            # Submit via Enter and send button if needed
            await textarea.press("Enter")
            try:
                btn = page.locator("button[aria-label='Send'], button[aria-label='Send prompt'], button[data-testid='send-button']").first
                if await btn.is_visible(timeout=1000):
                    await btn.click()
            except Exception:
                pass

            print("Waiting for ChatGPT response...")
            # Wait for generation to start (stop button appearing)
            try:
                await page.wait_for_selector(
                    "button[aria-label*='Stop'], button[data-testid*='stop']",
                    timeout=8000
                )
                print("Generation in progress...")
                # Wait for generation to complete (stop button disappearing)
                await page.wait_for_selector(
                    "button[aria-label*='Stop'], button[data-testid*='stop']",
                    state="detached",
                    timeout=180000
                )
            except Exception:
                # Fallback: wait for output to stabilize
                print("Monitoring response stream...")
                last_len = 0
                stable_count = 0
                for _ in range(60):
                    await asyncio.sleep(2)
                    text = await page.evaluate("""() => {
                        const turns = document.querySelectorAll("div.group.flex.flex-col");
                        const asst = Array.from(turns).filter(t => !t.querySelector("[class*='user-message']"));
                        return asst.length > 0 ? asst[asst.length - 1].innerText.length : 0;
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
            response_text = await page.evaluate("""() => {
                const turns = document.querySelectorAll("div.group.flex.flex-col");
                const asst = Array.from(turns).filter(t => !t.querySelector("[class*='user-message']"));
                if (asst.length > 0) {
                    return asst[asst.length - 1].innerText.trim();
                }
                const articles = document.querySelectorAll("[data-message-author-role='assistant'], .markdown");
                if (articles.length > 0) {
                    return articles[articles.length - 1].innerText.trim();
                }
                return "";
            }""")

            return response_text if response_text else "Error reading ChatGPT output."

        finally:
            await page.close()
