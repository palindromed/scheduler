from __future__ import unicode_literals, print_function
import os
from api_call import get_one_sol
import redis
import smtplib


def main():
    redis_url = os.getenv('REDISTOGO_URL', None)
    if redis_url is not None:
        red = redis.from_url(redis_url)
        new = os.getenv("NEW_REDIS")
        if new:
            sol = 0
            red.set('SOL', sol)
        else:
            sol = int(red.get('SOL'))
        get_one_sol('curiosity', sol)
        sol += 1
        red.set('SOL', sol)
        send_mail(sol)
        print(sol)


def send_mail(sol):

    sender = 'cummins.hannah@gmail.com'
    receivers = ['hannahkrager@gmail.com']

    message = """From: Me <cummins.hannah@gmail.com>
    To: Hannah <hannahkrager@gmail.com>
    Subject: SMTP e-mail test

    The script has run. SOL is at: {}""".format(sol)

    try:
        smtp_obj = smtplib.SMTP('localhost')
        smtp_obj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")

if __name__ == '__main__':
    main()
