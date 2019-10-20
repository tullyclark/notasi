from app import app
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import config
import atexit

jobstores = {
    'default': SQLAlchemyJobStore(url=f'postgresql://notasi:{config.notasi_password}@localhost/notasi')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(1)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 1,
    'misfire_grace_time': None,
    'replace_existing': True
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

scheduler.start()

atexit.register(lambda: scheduler.shutdown())






if __name__ == "__main__":
    app.run()
