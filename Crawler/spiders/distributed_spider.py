import scrapy

class DistributedSpider(scrapy.Spider):
    name = "distributed_spider"

    def __init__(self, start_url = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if start_url is None:
            self.logger.info(f"Crawler: No url provided")
            return
        else:
            self.start_urls = [start_url]

    def parse(self, response):
        links = response.css('a::attr(href)').getall()
        html = response.text
        yield {"url": response.url, "links": links, "html": html}
