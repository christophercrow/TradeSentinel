#!/bin/bash
# This script creates the full project structure with code files.

set -e

# Create directories
mkdir -p TradeSentinel/spiders
mkdir -p tests

# Create scrapy.cfg in the project root
cat > scrapy.cfg << 'EOF'
[settings]
default = TradeSentinel.settings

[deploy]
# (No deploy configuration for now)
EOF

# Create TradeSentinel/__init__.py (empty)
touch TradeSentinel/__init__.py

# Create TradeSentinel/items.py
cat > TradeSentinel/items.py << 'EOF'
import scrapy

class CapitolTradeItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    # Add additional fields if needed (e.g., date, politician, etc.)
EOF

# Create TradeSentinel/middlewares.py
cat > TradeSentinel/middlewares.py << 'EOF'
from scrapy import signals

class TradeSentinelSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
EOF

# Create TradeSentinel/pipelines.py
cat > TradeSentinel/pipelines.py << 'EOF'
class TradeSentinelPipeline:
    def process_item(self, item, spider):
        spider.logger.info("Processing item: %s" % item)
        # (Here you could clean, validate, or store the item)
        return item
EOF

# Create TradeSentinel/settings.py
cat > TradeSentinel/settings.py << 'EOF'
BOT_NAME = 'TradeSentinel'

SPIDER_MODULES = ['TradeSentinel.spiders']
NEWSPIDER_MODULE = 'TradeSentinel.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure item pipelines
ITEM_PIPELINES = {
    'TradeSentinel.pipelines.TradeSentinelPipeline': 300,
}

# (Optional) Configure downloader and spider middlewares if needed
DOWNLOADER_MIDDLEWARES = {
    # The httpcompression middleware is enabled by default (set here for clarity)
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Enable Scrapy-Playwright download handler
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Use the asyncio reactor (required for scrapy-playwright)
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Playwright launch options
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
}
EOF

# Create TradeSentinel/spiders/__init__.py (empty)
touch TradeSentinel/spiders/__init__.py

# Create TradeSentinel/spiders/capitol_trades_spider.py
cat > TradeSentinel/spiders/capitol_trades_spider.py << 'EOF'
import scrapy
from scrapy_playwright.page import PageMethod
from TradeSentinel.items import CapitolTradeItem

class CapitolTradesSpider(scrapy.Spider):
    name = "capitol_trades"
    start_urls = ['https://www.capitoltrades.com/trades']

    # Use Playwright to wait for the page to load (optional)
    custom_settings = {
        "PLAYWRIGHT_PAGE_METHODS": [
            PageMethod("wait_for_selector", "body"),
        ],
    }

    def parse(self, response):
        item = CapitolTradeItem()
        item['title'] = response.xpath("//title/text()").get()
        item['url'] = response.url
        yield item
EOF

# Create tests/test.py
cat > tests/test.py << 'EOF'
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from TradeSentinel.spiders.capitol_trades_spider import CapitolTradesSpider

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(CapitolTradesSpider)
    process.start()
EOF

echo "Project structure created successfully."
