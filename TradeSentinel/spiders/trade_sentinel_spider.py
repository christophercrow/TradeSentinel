import scrapy
from scrapy import signals

class TradeSentinelSpider(scrapy.Spider):
    name = "tradesentinel"
    start_urls = ["http://example.com/data"]  # Example start URL

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(TradeSentinelSpider, cls).from_crawler(crawler, *args, **kwargs)
        # Connect signals for spider open/close to custom handlers
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_opened(self, spider):
        self.logger.info(f"Spider started: {spider.name}")

    def spider_closed(self, spider, reason):
        self.logger.info(f"Spider closed: {spider.name} (reason: {reason})")

    def parse(self, response):
        # Parse the page and yield items
        for entry in response.css("div.item"):
            title = entry.css("h2::text").get()
            date = entry.css("span.date::text").get()
            summary = entry.css("p::text").get()
            url = response.url

            # If crucial data is missing, log an error and skip this item
            if not title or not date:
                self.logger.error(f"Missing title or date for entry on {response.url}")
                continue

            # Create the item (could also use a Scrapy Item class)
            item = {
                "title": title,
                "date": date,
                "summary": summary,
                "url": url
            }
            # Log the scraped item
            self.logger.info(f"Scraped item: {item['title']}")
            yield item

        # (If pagination is needed, handle next page requests here)
