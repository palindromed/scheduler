import os
import redis


def redis_init():
    redis_url = os.getenv('REDISTOGO_URL', None)
    red = redis.from_url(redis_url)
    red.set('SOL', 51)
    # red.set('PAGE', 3)
    # opportunity = 75
    # curiosity = 51
    # spirit = 164

if __name__ == "__main__":
    redis_init()
