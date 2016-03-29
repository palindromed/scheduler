from __future__ import unicode_literals, print_function
import os
from api_call import get_one_sol
import redis
# import smtplib
# from email.mime.text import MIMEText
import requests


def main():
    redis_url = os.getenv('REDISTOGO_URL', None)
    if redis_url is not None:
        red = redis.from_url(redis_url)
        new = os.getenv("NEW_REDIS")
    else:
        params = {
            "subject": "Redis Error",
            "text": "Could not connect to Redis"
        }
        send_mail(params)
        return
    if new:
        sol = 0
        red.set('SOL', sol)
        # os.environ['new'] = 'False'
    else:
        sol = int(red.get('SOL'))
    try:
        get_one_sol('curiosity', sol)
        sol += 1
        red.set('SOL', sol)
        params = {
            "subject": 'Success!!',
            "text": "All went well in API call. SOL for call was {}".format(sol)
        }
        send_mail(params)
        print(sol)
    except requests.exceptions.HTTPError:
        params = {
            "subject": "API Error",
            "text": "There was a problem connecting to the API."
        }
        send_mail(params)


def send_mail(**kwargs):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox683f8d129b354362b092d1be8762ae7e.mailgun.org",
        auth=("api", os.environ.get("MAILGUN_API_KEY")),
        data={"from": "Mars Rover Bot",
              "to": ["Hannah", "hannahkrager@gmail.com"],
              "subject": "{subject}".format(),
              "text": "{text}".format()})


if __name__ == '__main__':
    main()
