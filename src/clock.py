from __future__ import unicode_literals
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import (EVENT_JOB_EXECUTED, EVENT_JOB_ERROR,
                                EVENT_JOB_MISSED)
from worker import main

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', seconds=10)
def timed_job():
    main('curiosity')


def my_listener(event):
    if event.exception:
        print('The job crashed :(', event)
    else:
        print('The job worked :)')

scheduler.add_listener(timed_job, EVENT_JOB_EXECUTED |
                       EVENT_JOB_ERROR | EVENT_JOB_MISSED)
scheduler.start()
