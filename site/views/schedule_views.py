import flask
import pandas
import data.db_session as db_session
from flask_login import login_required


blueprint = flask.Blueprint('schedule', __name__, template_folder = 'templates')
@blueprint.before_request
@login_required
def before_request():
    """ Protect all of the admin endpoints. """
    pass 


@blueprint.route('/')

def index():

	schedules = pandas.read_sql("select * from apscheduler_jobs", db_session.notasi_engine()).to_dict('records')
	print(schedules)
	return flask.render_template(
		'schedule/index.html'
		,schedules = schedules
	)