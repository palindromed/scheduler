import os
import redis


def redis_init():
    redis_url = os.getenv('REDISTOGO_URL', None)
    red = redis.from_url(redis_url)
    red.set('SOL', 4)
    # red.set('PAGE', 3)

if __name__ == "__main__":
    redis_init()
