from __future__ import unicode_literals, print_function
import os
from api_call import get_one_sol
import redis
import requests


def main(rover):
    redis_url = os.getenv('REDISTOGO_URL', None)
    if redis_url is not None:
        red = redis.from_url(redis_url)
    else:
        return 'Redis error'
    sol = int(red.get('SOL'))
    print('check initial sol', sol)
    try:
            to_increase = get_one_sol(rover, sol)
            print('to increase', to_increase)
            sol += 1
            print(sol)
            red.set('SOL', sol)
    except requests.exceptions.HTTPError:
        print('API error or no data for {} on {}.'.format(sol))
        sol += 1
        red.set('SOL', sol)
