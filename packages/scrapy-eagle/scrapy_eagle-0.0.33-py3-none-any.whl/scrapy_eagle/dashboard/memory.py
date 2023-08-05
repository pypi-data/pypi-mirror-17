import redis

from scrapy_eagle.dashboard.settings import get_config_file

redis_pool = None


def init_memory():

    global redis_pool

    config = get_config_file()

    redis_pool = redis.ConnectionPool(
        host=config['redis']['host'],
        port=config['redis']['port'],
        db=config['redis']['db'],
        password=config.get('redis', 'password', fallback='')
    )


def get_redis_pool():
    return redis_pool


def get_connection():

    if not redis_pool:
        init_memory()

    return redis.Redis(connection_pool=redis_pool)
