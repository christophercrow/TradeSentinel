from datetime import datetime
from scrapy.exceptions import DropItem

class DataCleaningPipeline:
    def __init__(self):
        # Track seen item titles to remove duplicates
        self.seen_titles = set()

    def process_item(self, item, spider):
        # Clean whitespace in all string fields
        for field, value in item.items():
            if isinstance(value, str):
                item[field] = value.strip()

        # Drop duplicate items based on title (or another unique identifier)
        title = item.get('title')
        if title:
            if title in self.seen_titles:
                spider.logger.info(f"Duplicate item dropped: {title}")
                raise DropItem(f"Duplicate item found: {title}")
            self.seen_titles.add(title)

        # Standardize date format to YYYY-MM-DD if a date field exists
        date_str = item.get('date')
        if date_str:
            parsed_date = None
            # Try multiple date formats for flexibility
            for fmt in ("%B %d, %Y", "%Y-%m-%d", "%d %b %Y"):
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    break
                except ValueError:
                    continue
            if parsed_date:
                item['date'] = parsed_date.strftime("%Y-%m-%d")
            else:
                spider.logger.error(f"Invalid date format for item '{title}': {date_str}")
                raise DropItem(f"Invalid date format for item: {title}")

        # Validate required fields (e.g., title and date must be present)
        if not item.get('title') or not item.get('date'):
            spider.logger.error(f"Missing required fields in item: {item}")
            raise DropItem(f"Missing required fields in item: {item}")

        # If all validations pass, log and return the clean item
        spider.logger.info(f"Item passed validation: {item.get('title')}")
        return item
