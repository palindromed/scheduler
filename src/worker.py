from __future__ import unicode_literals, print_function
import os
from api_call import get_one_sol, populate_from_data
import redis
import requests


def main(rover):
    redis_url = os.getenv('REDISTOGO_URL', None)
    if redis_url is not None:
        red = redis.from_url(redis_url)
    else:
        return 'Redis error'
    sol = int(red.get('SOL'))
    page = int(red.get('PAGE'))
    print('check initial sol/page', sol, page)
    # try:
    to_increase = get_one_sol(rover, sol, page)
    print('to increase', to_increase)
    #     if to_increase == 'sol':
    #         sol += 1
    #         red.set('SOL', sol)
    #         red.set('PAGE', 1)
    #         print(sol, page)
    #     elif to_increase == 'page':
    #         page += 1
    #         red.set('PAGE', page)
    #         print(sol, page)
    # except requests.exceptions.HTTPError:
    #     print('API error or no data for {} on {}.'.format(sol, page))
    #     sol += 1
    #     red.set('SOL', sol)
    #     red.set('PAGE', 1)


def send_mail(subject, text):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox683f8d129b354362b092d1be8762ae7e.mailgun.org/messages",
        auth=("api", os.environ.get('MAILGUN_API_KEY')),
        data={"from": "Mars Rover Bot <postmaster@sandbox683f8d129b354362b092d1be8762ae7e.mailgun.org>",
              "to": ["Hannah  <hannahkrager@gmail.com>"],
              "subject": "{}".format(subject),
              "text": "{}".format(text)})




# if __name__ == '__main__':
#     main('curiosity')
