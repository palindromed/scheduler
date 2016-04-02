from __future__ import unicode_literals
from apscheduler.schedulers.blocking import BlockingScheduler
from worker import main
import logging

log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG

fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)


scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', minutes=2)
def timed_job():
    return_value = main('Spirit')
    print(return_value)


scheduler.start()
