from __future__ import unicode_literals
from apscheduler.schedulers.blocking import BlockingScheduler
from worker import main
from sqlalchemy import create_engine
from models import DBSession, Base
import os


database_url = os.environ.get("MARS_DATABASE_URL", None)
engine = create_engine(database_url)
DBSession.configure(bind=engine)
Base.metadata.create_all(engine)


scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', seconds=8)
def timed_job():
    return_value = main('opportunity')
    print(return_value)


scheduler.start()
