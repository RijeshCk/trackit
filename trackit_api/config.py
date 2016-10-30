from redis import StrictRedis


KEY_TIMEOUT = 30
REDIS_KEY_DB = 1
redis_connection = StrictRedis(db=REDIS_KEY_DB)