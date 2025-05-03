import json
from Assets.db import conn, cursor

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html




# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CrawlerPipeline:
    def open_spider(self, spider):
        self.conn = conn
        self.cursor = cursor

    def close_spider(self, spider):
        self.conn.commit()

    def process_item(self, item, spider):
        # Check if 'html' is present, set to empty string if missing
        html_content = item.get('html', '')  # Default to empty string if 'html' is missing
        
        # Prepare data for insertion
        sql = "INSERT INTO crawled_pages (URL, html, links, retrieved) VALUES (%s, %s, %s, %s)"
        values = (
            item['url'],
            html_content,  # Use html_content instead of directly accessing item['html']
            json.dumps(item['links']),
            False
        )

        self.cursor.execute(sql, values)
        return item
