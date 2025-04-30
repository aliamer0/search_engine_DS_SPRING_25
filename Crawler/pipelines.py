import mysql.connector
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html




# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CrawlerPipeline:

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
                host = "156.214.166.39",
                port = "26257",
                user = "ali",
                database = "search_engine",
                sslmode = "disable"
                

            )


    def close_spider(self, spider):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
    
    def process_item(self, item, spider):
        sql = "INSERT INTO crawled_pages (URL, html, links, retrieved) VALUES (%s, %s, %s)"
        values = (
                item['url'],
                item['html'],
                json.dumps(item['links']),
                False
            )

        self.cursor.execute(sql, values)
        
        return item
