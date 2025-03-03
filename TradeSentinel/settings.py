import logging
from scrapy.utils.log import configure_logging
from logging.handlers import RotatingFileHandler

# --- Logging Configuration ---
LOG_ENABLED = True
configure_logging(install_root_handler=False)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Log to file (rotating every 5MB)
file_handler = RotatingFileHandler('tradesentinel.log', maxBytes=5*1024*1024, backupCount=1)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
root_logger.addHandler(file_handler)

# Log to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
root_logger.addHandler(console_handler)

# --- Scrapy and Playwright Settings ---
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
PLAYWRIGHT_BROWSER_TYPE = "chromium"
# Uncomment the next line to see the browser window (non-headless mode)
# PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": False}

# --- Item Pipelines ---
ITEM_PIPELINES = {
    'TradeSentinel.pipelines.DataCleaningPipeline': 300,
}

# --- Feed Export Settings ---
FEEDS = {
    'output.json': {
        'format': 'json',
        'encoding': 'utf8',
        'indent': 4,
        'overwrite': True,
    }
}

ROBOTSTXT_OBEY = True
SPIDER_LOADER_WARN_ONLY = True
