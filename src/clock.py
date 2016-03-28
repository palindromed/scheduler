from __future__ import unicode_literals

from apscheduler.schedulers.blocking import BlockingScheduler
import lib2to3
import requests

from api_call import get_one_sol
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    job_num = 0
    # get_one_sol('curiosity', 780)
    response = requests.get('http://codefellows.org')
    job_num += 1
    print(job_num, response.status_code)


sched.start()
