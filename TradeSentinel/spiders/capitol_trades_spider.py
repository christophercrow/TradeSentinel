import scrapy
from scrapy_playwright.page import PageMethod

class CapitolTradesSpider(scrapy.Spider):
    name = "capitol_trades"
    allowed_domains = ["capitoltrades.com"]
    start_urls = ["https://www.capitoltrades.com/trades"]

    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        # Uncomment to run with a visible browser window:
        # "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": False},
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        # Wait for the main table to appear
                        PageMethod("wait_for_selector", "table"),
                    ],
                },
                callback=self.parse,
            )

    def parse(self, response):
        self.logger.info("Parsing CapitolTrades page")
        # Select only rows that contain <td> elements (to avoid header rows)
        rows = response.xpath("//table//tr[td]")
        self.logger.info(f"Found {len(rows)} trade rows in the table")

        for row in rows:
            cells = row.xpath("td")
            # Skip any row that doesn't have at least 7 cells
            if len(cells) < 7:
                self.logger.debug("Skipping row with insufficient cells")
                continue

            # Extract text from each cell; you may need to adjust these XPath expressions
            item = {
                "time": cells[0].xpath("normalize-space()").get(),
                "politician": cells[1].xpath("normalize-space()").get(),
                "trade_date": cells[2].xpath("normalize-space()").get(),
                "ticker": cells[3].xpath("normalize-space()").get(),
                "trade_type": cells[4].xpath("normalize-space()").get(),
                "amount": cells[5].xpath("normalize-space()").get(),
                "source": cells[6].xpath("normalize-space()").get(),
            }
            yield item
