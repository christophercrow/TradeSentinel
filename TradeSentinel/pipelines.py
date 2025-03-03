from scrapy.exceptions import DropItem

class DataCleaningPipeline:
    def __init__(self):
        # Use a set to track already seen items using a composite key
        self.seen = set()

    def process_item(self, item, spider):
        # Clean whitespace from all string fields
        for key, value in item.items():
            if isinstance(value, str):
                item[key] = value.strip()

        # (Optional) Further normalization—for example, splitting combined fields—
        # you can adjust the following if needed:
        #
        # if item.get("time"):
        #     # For instance, if the time cell sometimes concatenates multiple pieces,
        #     # you might split them here.
        #     parts = item["time"].split()
        #     item["time"] = parts[0] if parts else item["time"]

        # Create a composite key using a few fields
        unique_key = (
            item.get("time"),
            item.get("politician"),
            item.get("trade_date"),
            item.get("ticker"),
        )
        if unique_key in self.seen:
            raise DropItem(f"Duplicate item found: {unique_key}")
        self.seen.add(unique_key)
        return item
