from celery import shared_task
import redis
from redis.exceptions import RedisError
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=5, default_retry_delay=5, acks_late=True)
def distribute_url(self, url):
    try:
        r = redis.StrictRedis(host="localhost", port=6379, db=0)
        r.lpush('urls', url)
        logger.info(f"Received and stored URL: {url}")
    except RedisError as exc:
        logger.error(f"Redis connection failed: {exc}. Retrying...")
        raise self.retry(exc=exc)
