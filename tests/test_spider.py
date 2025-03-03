import pytest
from scrapy.http import TextResponse
from scrapy.exceptions import DropItem
from TradeSentinel.spiders.trade_sentinel_spider import TradeSentinelSpider
from TradeSentinel.pipelines import DataCleaningPipeline

def create_response(html, url="http://example.com"):
    """Utility to create a TextResponse object from HTML string."""
    return TextResponse(url=url, body=html.encode('utf-8'), encoding='utf-8')

def test_parse_basic_item():
    """Test that the spider extracts a title and URL."""
    spider = TradeSentinelSpider()
    html_content = """
    <html>
      <body>
        <h1>Example Domain</h1>
      </body>
    </html>
    """
    response = create_response(html_content)
    results = list(spider.parse(response))
    assert len(results) == 1
    item = results[0]
    assert item.get('title') == "Example Domain"
    assert item.get('url') == "http://example.com"

def test_pipeline_duplicate_and_validation():
    """Test the data cleaning pipeline for duplicate removal and required field validation."""
    pipeline = DataCleaningPipeline()
    spider = TradeSentinelSpider()

    item1 = {"title": "Test Title", "url": "http://example.com", "extra": "data"}
    item2 = {"title": "Test Title", "url": "http://example.com", "extra": "other data"}

    cleaned1 = pipeline.process_item(item1, spider)
    assert cleaned1["title"] == "Test Title"
    with pytest.raises(DropItem):
        pipeline.process_item(item2, spider)
