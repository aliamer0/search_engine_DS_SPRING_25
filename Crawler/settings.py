# settings.py

# Scrapy settings for your project
BOT_NAME = 'Crawler'

SPIDER_MODULES = ['Crawler.spiders']
NEWSPIDER_MODULE = 'Crawler.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Enable or disable spider middlewares
SPIDER_MIDDLEWARES = {
   'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 543,
   'Crawler.middlewares.CustomErrorMiddleware': 100,
}

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # Disable the default UserAgentMiddleware
    'Crawler.middlewares.CustomRetryMiddleware': 120,  # Custom Retry Middleware
    'Crawler.middlewares.CustomUserAgentMiddleware': 400,  # Custom User-Agent Middleware
}

# Enable or disable extensions
EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
}

# Configure item pipelines
ITEM_PIPELINES = {
   'Crawler.pipelines.CrawlerPipeline': 1,
}

# Enable logging
LOG_LEVEL = 'DEBUG'
LOG_FILE = 'scrapy.log'

# Concurrent requests and download delay settings
CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8
DOWNLOAD_DELAY = 2  # seconds between requests

# Retry settings (for handling failed requests)
RETRY_ENABLED = True
RETRY_TIMES = 5  # Retry 5 times before failing
RETRY_HTTP_CODES = [500, 502, 503, 504, 408]

# Timeout settings
DOWNLOAD_TIMEOUT = 30  # Time out for each request

# Custom headers to avoid detection
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
   'Accept-Encoding': 'gzip, deflate, br',
   'Connection': 'keep-alive',
   'Upgrade-Insecure-Requests': '1',
   'Accept-Language': 'en-US,en;q=0.9',
}

# Enable AutoThrottle (adjusts download delay based on load)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Enable HTTP cache for faster crawling (useful for testing)
HTTPCACHE_ENABLED = False  # Set to True if you want caching

# Configure Scrapy's logging
LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'
LOG_FILE = 'scrapy_log.txt'
CLOSESPIDER_PAGECOUNT = 1
# Other general settings
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'  # Set a specific User-Agent for your crawler

# Timeouts
DOWNLOAD_TIMEOUT = 15  # Max time to wait for a response
CONCURRENT_REQUESTS = 16  # Max concurrent requests
