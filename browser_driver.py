import asyncio
from playwright.async_api import async_playwright

CDP_URL = "http://localhost:9222"

async def _connect_browser(p):
    try:
        return await p.chromium.connect_over_cdp(CDP_URL)
    except Exception as e:
        print("\n[!] Could not connect to Chrome on port 9222.")
        print("Run: python start_browser.py (or ./start_browser.sh on macOS/Linux)")
        raise e

async def run_chatgpt_prompt(prompt_text: str) -> str:
    async with async_playwright() as p:
        print("Connecting to your running Chrome session...")
        browser = await _connect_browser(p)
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


async def run_claude_prompt(prompt_text: str) -> str:
    async with async_playwright() as p:
        print("Connecting to your running Chrome session...")
        browser = await _connect_browser(p)
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