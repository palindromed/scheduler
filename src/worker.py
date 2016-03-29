from __future__ import unicode_literals, print_function
import os
from latest_api_call import get_one_sol
import redis
# import smtplib
# from email.mime.text import MIMEText
import requests


def connect_to_redis():
    redis_url = os.getenv('REDISTOGO_URL', None)
    if redis_url is not None:
        return redis.from_url(redis_url)
    else:
        subject = "Redis Error"
        text = "Could not connect to Redis. Unable to get SOL and page"
        send_mail(subject, text)


def main(rover):
    red = connect_to_redis()
    new = os.getenv("NEW_REDIS")
    if new:
        sol = 0
        red.set('SOL', sol)
        page = 1
        red.set('PAGE', page)
        os.environ['new'] = 'False'
    else:
        sol = int(red.get('SOL'))
        page = int(red.get('PAGE'))
    try:
        # save in label, check to see if sol or page should increase
        to_increase = get_one_sol(sol, page)
        if to_increase == 'sol':
            sol += 1
            red.set('SOL', sol)
            red.set('PAGE', 1)
        elif to_increase == 'page':
            page += 1
            red.set('page', page)
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
