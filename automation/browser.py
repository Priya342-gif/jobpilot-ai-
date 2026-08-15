from playwright.async_api import async_playwright

class BrowserAgent:
    async def open_job(self, url: str):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            title = await page.title()
            await browser.close()
            return {"title": title, "url": url}

    async def inspect_application(self, url: str):
        # Inspection only. Submission is deliberately not automated here.
        return await self.open_job(url)
