import sqlalchemy as sa
import datetime

from data.modelbase import SqlAlchemyBase
from sqlalchemy.dialects import postgresql
from flask_login import UserMixin



class SqlType(SqlAlchemyBase):

	__tablename__ = 'sql_types'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String)
	dialect = sa.Column(sa.String)
	locations = sa.orm.relationship("Location")

class RequestMethod(SqlAlchemyBase):

	__tablename__ = 'request_methods'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String)
	queries = sa.orm.relationship("Query")

class LocationType(SqlAlchemyBase):

	__tablename__ = 'location_types'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String)
	locations = sa.orm.relationship("Location")

class Location(SqlAlchemyBase):

	__tablename__ = 'locations'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String)
	location_type_id = sa.Column(sa.Integer, sa.ForeignKey('location_types.id'))
	location_type = sa.orm.relationship("LocationType")
	address = sa.Column(sa.String)
	port = sa.Column(sa.String)
	username = sa.Column(sa.String)
	password = sa.Column(sa.String)
	sql_type_id = sa.Column(sa.Integer, sa.ForeignKey('sql_types.id'))
	sql_type = sa.orm.relationship("SqlType")
	database = sa.Column(sa.String)
	queries = sa.orm.relationship("Query", cascade="all, delete-orphan")
	created_date = sa.Column(sa.DateTime, default = datetime.datetime.now)

class Query(SqlAlchemyBase):
	
	__tablename__ = 'queries'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String)
	notasi_query = sa.Column(sa.String)
	endpoint = sa.Column(sa.String)
	head = sa.Column(sa.String)
	body = sa.Column(sa.String)
	request_method_id = sa.Column(sa.Integer, sa.ForeignKey('request_methods.id'))
	request_method = sa.orm.relationship("RequestMethod")
	location_id = sa.Column(sa.Integer, sa.ForeignKey('locations.id'))
	location = sa.orm.relationship("Location")
	views = sa.orm.relationship("DataView")
	created_date = sa.Column(sa.DateTime, default = datetime.datetime.now)

class DataView(SqlAlchemyBase):
	
	__tablename__ = 'data_views'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String, nullable=False)
	view_name = sa.Column(sa.String, nullable=False)
	business_keys = sa.Column(sa.String, nullable=False)
	information_columns = sa.Column(sa.String, nullable=False)
	query_id = sa.Column(sa.Integer, sa.ForeignKey('queries.id'), nullable=False)
	query = sa.orm.relationship("Query")
	user_data = sa.orm.relationship("UserData")
	created_date = sa.Column(sa.DateTime, default = datetime.datetime.now)

class UserData(SqlAlchemyBase):
	
	__tablename__ = 'user_data'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	data = sa.Column(postgresql.JSONB)
	data_view_id = sa.Column(sa.Integer, sa.ForeignKey('data_views.id', ondelete='SET NULL'))
	data_view = sa.orm.relationship("DataView")
	created_date = sa.Column(sa.DateTime, default = datetime.datetime.now)

class Schedules(SqlAlchemyBase):
	
	__tablename__ = 'schedules'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String)
	cron_schedule = sa.Column(sa.String)
	apscheduler_job_id = sa.Column(sa.String, sa.ForeignKey('apscheduler_jobs.id'))
	apscheduler_job = sa.orm.relationship("APSchedulerJobs")

class ScheduleSteps(SqlAlchemyBase):
	
	__tablename__ = 'schedule_steps'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	schedule_id = sa.Column(sa.Integer, sa.ForeignKey('schedules.id'))
	schedule = sa.orm.relationship("Schedules")
	order = sa.Column(sa.Integer)
	query_id = sa.Column(sa.Integer, sa.ForeignKey('queries.id'))
	query = sa.orm.relationship("Query")

class APSchedulerJobs(SqlAlchemyBase):
	__tablename__ = 'apscheduler_jobs'
	id = sa.Column(sa.String, primary_key=True)
	next_run_time = sa.Column(sa.Integer)

class User(UserMixin, SqlAlchemyBase):
	__tablename__ = 'notasi_users'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	username = sa.Column(sa.String, unique=True)
	password = sa.Column(sa.String)
	name = sa.Column(sa.String)
