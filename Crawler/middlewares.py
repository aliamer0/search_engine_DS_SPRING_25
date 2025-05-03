# middlewares.py

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
from scrapy.spidermiddlewares.httperror import HttpError
import random


class CustomErrorMiddleware:
    """Custom middleware to handle errors with logging and retries."""

    def process_exception(self, request, exception, spider):
        """Handle specific exceptions and log them."""
        if isinstance(exception, HttpError):
            spider.logger.error(f"HTTP Error on {request.url}: {exception.value.response.status}")
        elif isinstance(exception, DNSLookupError):
            spider.logger.error(f"DNS Lookup Error on {request.url}")
        elif isinstance(exception, (TimeoutError, TCPTimedOutError)):
            spider.logger.error(f"Timeout Error on {request.url}")
        else:
            spider.logger.error(f"Unexpected Error on {request.url}: {str(exception)}")
        return None


class CustomRetryMiddleware(RetryMiddleware):
    """Customized RetryMiddleware to handle retry for specific HTTP errors"""

    def process_response(self, request, response, spider):
        """Handle retry logic for certain HTTP error codes"""
        if response.status in self.retry_http_codes:
            return self._retry(request, 'HTTP Error', response, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        """Handle retry logic on exceptions"""
        return self._retry(request, exception, None, spider)


class CustomUserAgentMiddleware(UserAgentMiddleware):
    """Custom middleware to randomly set User-Agent for each request."""
    
    def __init__(self, user_agent=''):
        super().__init__(user_agent)
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
            # Add more user-agents as needed
        ]

    def process_request(self, request, spider):
        """Set a random User-Agent header for each request."""
        request.headers['User-Agent'] = random.choice(self.user_agents)
