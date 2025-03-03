import pytest
from scrapy.http import TextResponse
from scrapy.exceptions import DropItem
from TradeSentinel.spiders.trade_sentinel_spider import TradeSentinelSpider
from TradeSentinel.pipelines import DataCleaningPipeline

def create_response(html, url="http://example.com"):
    """Utility to create a TextResponse object from HTML string for testing."""
    return TextResponse(url=url, body=html.encode('utf-8'), encoding='utf-8')

def test_parse_basic_item():
    """Spider should parse a basic item correctly."""
    spider = TradeSentinelSpider()
    html_content = """
    <html><body>
      <div class='item'>
        <h2>Sample Title</h2>
        <span class='date'>March 3, 2025</span>
        <p>Some summary text.</p>
      </div>
    </body></html>
    """
    response = create_response(html_content)
    results = list(spider.parse(response))
    # One item should be yielded
    assert len(results) == 1
    item = results[0]
    # Fields should be extracted as expected
    assert item.get('title') == "Sample Title"
    assert item.get('date') == "March 3, 2025"
    assert item.get('summary') == "Some summary text."
    assert item.get('url') == "http://example.com"

def test_parse_missing_fields():
    """Spider should skip items with missing required fields (e.g., no date)."""
    spider = TradeSentinelSpider()
    html_content = """
    <html><body>
      <div class='item'>
        <h2>Title Without Date</h2>
        <!-- Missing date span -->
        <p>Summary text.</p>
      </div>
    </body></html>
    """
    response = create_response(html_content)
    results = list(spider.parse(response))
    # The item with missing date should be skipped (no items yielded)
    assert results == []

def test_pipeline_duplicate_and_validation():
    """DataCleaningPipeline should remove duplicates and validate fields."""
    pipeline = DataCleaningPipeline()
    spider = TradeSentinelSpider()

    item1 = {"title": "Duplicate Title", "date": "2025-03-03", "summary": "A", "url": "http://x"}
    item2 = {"title": "Duplicate Title", "date": "2025-03-03", "summary": "B", "url": "http://y"}

    # First item passes through
    cleaned1 = pipeline.process_item(item1, spider)
    assert cleaned1["date"] == "2025-03-03"  # already standardized

    # Second item with same title should be dropped as a duplicate
    with pytest.raises(DropItem):
        pipeline.process_item(item2, spider)

def test_pipeline_date_standardization():
    """DataCleaningPipeline should standardize various date formats."""
    pipeline = DataCleaningPipeline()
    spider = TradeSentinelSpider()

    # Date in long format should be converted
    item = {"title": "Date Format Test", "date": "March 3, 2025", "summary": "X", "url": "http://z"}
    cleaned = pipeline.process_item(item, spider)
    assert cleaned["date"] == "2025-03-03"

    # Unsupported date format should cause a DropItem exception
    bad_item = {"title": "Bad Date", "date": "3/3/2025", "summary": "Y", "url": "http://z"}
    with pytest.raises(DropItem):
        pipeline.process_item(bad_item, spider)
