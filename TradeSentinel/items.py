import scrapy

class CapitolTradeItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    # Add additional fields if needed (e.g., date, politician, etc.)
