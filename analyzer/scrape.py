from playwright.async_api import async_playwright
from collections import Counter


async def scrape_homepage(url: str, max_repeats: int = 2) -> str:
    """
    Scrapes the fully rendered homepage of a URL using Playwright.

    This function renders the full page (JavaScript included), extracts all visible
    text content from the <body> tag, removes short and blank lines, and deduplicates
    repeated lines to ensure a cleaner output for passing to the LLM for analysis.

    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_load_state("networkidle")
        content = await page.locator("body").inner_text()
        await browser.close()

    lines = [line.strip() for line in content.splitlines() if len(line.strip()) > 5]
    counter = Counter()
    final_lines = []

    for line in lines:
        if counter[line] < max_repeats:
            final_lines.append(line)
            counter[line] += 1

    return "\n".join(final_lines)
