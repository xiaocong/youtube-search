from flask.ext.cache import Cache
import os

cache = Cache(config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDISCLOUD_URL', 'redis://localhost')
})
