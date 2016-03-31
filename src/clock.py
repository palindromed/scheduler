from __future__ import unicode_literals
from apscheduler.schedulers.blocking import BlockingScheduler
from worker import main



scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', minutes=1)
def timed_job():
    return_value = main('opportunity')
    print(return_value)


scheduler.start()
