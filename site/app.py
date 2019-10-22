import flask
import os
import data.db_session as db_session
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from flask_login import LoginManager
import config
from views import home_views, schedule_views, auth_views, api_views, user_views, delete_view
from views.process_views import edit_view, process_views


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = config.flask_secret_key

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from data.source import User

@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return session.query(User).get(int(user_id))

    session.close()
# def start_scheduler():
# 	jobstores = {
# 	    'default': SQLAlchemyJobStore(url=f'postgresql://notasi:{config.notasi_password}@localhost/notasi')
# 	}
# 	executors = {
# 	    'default': ThreadPoolExecutor(20),
# 	    'processpool': ProcessPoolExecutor(1)
# 	}
# 	job_defaults = {
# 	    'coalesce': False,
# 	    'max_instances': 1,
# 	    'misfire_grace_time': None,
# 	    'replace_existing': True
# 	}

# 	scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
# 	return scheduler

# scheduler = start_scheduler()
# scheduler.start()

db_session.global_init()

app.register_blueprint(home_views.blueprint)
app.register_blueprint(auth_views.auth, url_prefix='/auth')
app.register_blueprint(api_views.blueprint, url_prefix='/api')
app.register_blueprint(process_views.blueprint, url_prefix='/process')
app.register_blueprint(edit_view.blueprint, url_prefix='/process/edit')
app.register_blueprint(user_views.blueprint, url_prefix='/user')
app.register_blueprint(schedule_views.blueprint, url_prefix='/schedule')
app.register_blueprint(delete_view.blueprint, url_prefix='/delete')

if __name__ == '__main__':
	app.run(debug = config.debug)