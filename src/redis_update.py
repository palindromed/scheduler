import os
import redis


def redis_init():
    redis_url = os.getenv('REDISTOGO_URL', None)
    red = redis.from_url(redis_url)
    red.set('SOL', 164)
    # opportunity = 404
    # curiosity = 295
    # spirit = 164

if __name__ == "__main__":
    redis_init()
