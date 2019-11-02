import flask
import os
import data.db_session as db_session
from pytz import utc
from data.source import User
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from flask_login import LoginManager
import config
from views import home_views, schedule_views, auth_views, sso_views, api_views, user_views, delete_view, chart_views, dashboard_views, group_views
from views.process_views import edit_view, process_views
from utils.lookup_init import  init_rows


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = config.flask_secret_key


db_session.global_init()
init_rows()


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return session.query(User).get(int(user_id))

    session.close()








app.register_blueprint(home_views.blueprint)
app.register_blueprint(auth_views.auth, url_prefix='/auth')
app.register_blueprint(sso_views.blueprint, url_prefix='/sso')
app.register_blueprint(api_views.blueprint, url_prefix='/api')
app.register_blueprint(dashboard_views.blueprint, url_prefix='/dashboard')
app.register_blueprint(chart_views.blueprint, url_prefix='/chart')
app.register_blueprint(process_views.blueprint, url_prefix='/process')
app.register_blueprint(edit_view.blueprint, url_prefix='/process/edit')
app.register_blueprint(user_views.blueprint, url_prefix='/user')
app.register_blueprint(group_views.blueprint, url_prefix='/group')
app.register_blueprint(schedule_views.blueprint, url_prefix='/schedule')
app.register_blueprint(delete_view.blueprint, url_prefix='/delete')

if __name__ == '__main__':
	app.run(debug = config.debug)