from __future__ import unicode_literals
from apscheduler.schedulers.blocking import BlockingScheduler
from worker import main


sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def timed_job():
    main()


sched.start()
