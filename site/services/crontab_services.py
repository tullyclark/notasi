from crontab import CronTab
import os
import sys
import getpass
import data.db_session as db_session
from data.source import Schedule


user = getpass.getuser()
my_cron = CronTab(user = user)


def delete_cron_job(id):
	for job in my_cron:
		if job.comment == str(id):
			my_cron.remove(job)
			my_cron.write()

def write_cron_job(id):
	session = db_session.create_session()
	schedule = session.query(Schedule).filter_by(id=id).first()
	queries = []
	for step in schedule.schedule_steps:
		queries.append(str(step.query_id))
	query_string = ",".join(queries)
	if queries:
		job = my_cron.new(command=f'{sys.executable} {os.getcwd()}/run_query.py --query {query_string} --out write', comment=str(id))
		job.setall(schedule.cron_schedule)
		my_cron.write()