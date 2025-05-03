import scrapy
from urllib.parse import urljoin

class DistributedSpider(scrapy.Spider):
    name = "DistributedSpider"

    def __init__(self, start_url=None, *args, **kwargs):
        super(DistributedSpider, self).__init__(*args, **kwargs)
        if not start_url:
            raise ValueError("You must provide a start_url argument")
        self.start_urls = [start_url]

    def parse(self, response):
        page_url = response.url
        page_html = response.text
        links = []
        for link in response.css('a[href]'):
            href = link.attrib.get('href')
            if href and "#" not in href:
                links.append(urljoin(response.url, href))

        yield {
            'url': page_url,
            'html': page_html,
            'links': links
        }
