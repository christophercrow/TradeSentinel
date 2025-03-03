import logging
from logging.handlers import RotatingFileHandler
from scrapy.utils.log import configure_logging

# Disable default Scrapy logging to set up custom handlers
LOG_ENABLED = False
configure_logging(install_root_handler=False)

# Set up the root logger to log to both a file and the console
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# File handler (rotating file up to 5 MB, with 1 backup)
file_handler = RotatingFileHandler('tradesentinel.log', maxBytes=5*1024*1024, backupCount=1)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
root_logger.addHandler(file_handler)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
root_logger.addHandler(console_handler)

# Configure the item pipelines
ITEM_PIPELINES = {
    'TradeSentinel.pipelines.DataCleaningPipeline': 300,
}

# Configure feed export to output.json (pretty-printed)
FEEDS = {
    'output.json': {
        'format': 'json',
        'encoding': 'utf8',
        'indent': 4,
        'overwrite': True,
    }
}

# Other settings (if needed)
ROBOTSTXT_OBEY = True
SPIDER_LOADER_WARN_ONLY = True
