from __future__ import unicode_literals, print_function
import os
from api_call import get_one_sol
import redis
import requests


def main():
    # r = redis.StrictRedis(host='localhost', port=6379, db=0)
    redis_url = os.getenv('REDISTOGO_URL', None)
    red = redis.from_url(redis_url)
    #answer = red.set('answer', 42)
    # job_num = red.get('sol')
    # get_one_sol('curiosity', 780)
    response = requests.get('http://codefellows.org')
    # job_num += 1
    answer = red.get('answer')
    answer = int(answer)
    answer += 1
    answer = red.set('answer', answer)
    # red.set(job_num)
    print(answer, response.status_code)


if __name__ == '__main__':
    main()
