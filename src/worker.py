from __future__ import unicode_literals, print_function
import os
from latest_api_call import get_one_sol
import redis
import requests
import os
import json
import transaction
from sqlalchemy import create_engine
# from mars_street_view.scripts import
from models import DBSession, Photo, Base

ROVERS = {
    'Curiosity': 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos',
    'Opportunity': 'https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos',
    'Spirit': 'https://api.nasa.gov/mars-photos/api/v1/rovers/spirit/photos',
}
NASA_API_KEY = os.environ.get('NASA_API_KEY')


def main(rover):
    redis_url = os.getenv('REDISTOGO_URL', None)
    if redis_url is not None:
        red = redis.from_url(redis_url)
    else:
        subject = "Redis Error"
        text = "Could not connect to Redis. Unable to get SOL and page"
        send_mail(subject, text)
    new = os.getenv("NEW_REDIS")
    if new:
        print('new')
        sol = 0
        red.set('SOL', sol)
        page = 1
        red.set('PAGE', page)
        os.environ['NEW_REDIS'] = 'False'
        print(sol, page)
    else:
        sol = int(red.get('SOL'))
        page = int(red.get('PAGE'))
        print(sol, page)
    try:
        # save in label, check to see if sol or page should increase
        to_increase = get_one_sol(rover, sol, page)
        if to_increase == 'sol':
            sol += 1
            red.set('SOL', sol)
            red.set('PAGE', 1)
            print(sol, page)
        elif to_increase == 'page':
            page += 1
            red.set('page', page)
            print(sol, page)
        subject = 'Success!!'
        text = "All went well in API call. SOL for call was {} on page {}.".format(sol, page)
        send_mail(subject, text)
        print(sol)
    except requests.exceptions.HTTPError:
        subject = "API Error",
        text = "There was a problem connecting to the API. SOL for call was {} on page {}.".format(sol, page)
        send_mail(subject, text)


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
