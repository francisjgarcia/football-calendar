import json


class FutbolPipeline:
    def __init__(self):
        self.items = []  # Array to store the items

    def process_item(self, item, spider):
        # Convert the item to a dictionary and append it to the items array
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        # Print a message with a line break
        print("All the matches in JSON format:")
        # Print the items in JSON format
        print(json.dumps(self.items, ensure_ascii=False, indent=4))
