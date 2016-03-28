from __future__ import unicode_literals

from apscheduler.schedulers.blocking import BlockingScheduler
import lib2to3
import requests

from .api_call import get_one_sol
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=5)
def timed_job():
    get_one_sol('curiosity', 780)


@sched.scheduled_job('cron', day_of_week='mon', hour=13)
def scheduled_job():
    print('I should print at 1pm')


sched.start()
