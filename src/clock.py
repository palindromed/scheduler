from __future__ import unicode_literals

from apscheduler.schedulers.blocking import BlockingScheduler
import lib2to3

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=5)
def timed_job():
    print('This should print every 5 minutes')


@sched.scheduled_job('cron', day_of_week='mon', hour=13)
def scheduled_job():
    print('I should print at 1pm')


sched.start()
