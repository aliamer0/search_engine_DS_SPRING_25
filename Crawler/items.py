import scrapy

class CrawlerItem(scrapy.Item):
    # Define the fields for the item
    url = scrapy.Field()          # The URL of the page
    links = scrapy.Field()        # List of extracted links from the page
    html = scrapy.Field()         # The HTML content of the page
