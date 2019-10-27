import flask
import pandas
import data.db_session as db_session
from flask_login import login_required
from data.source import User, Group
from services.select_services import get_objects, search_object
from werkzeug.security import generate_password_hash
from services.save_services import save_user, save_object
from decorators.admin import is_admin


blueprint = flask.Blueprint('users', __name__, template_folder = '../templates/user')
@blueprint.before_request
@login_required
@is_admin
def before_request():
    """ Protect all of the admin endpoints. """
    pass 


@blueprint.route('/')
def index():

	return flask.render_template(
		'user/index.html'
		, users = get_objects(User)
	)

@blueprint.route('/edit', methods=['POST', 'GET'])
def reset():
	id = flask.request.args.get('id', default = None, type = int)

	if flask.request.method == "GET":
		return flask.render_template(
			'user/edit_user.html'
			, item_type = 'user'
			, data_obj = search_object(id=id, item_type=User)
			, back_link = flask.request.referrer
		)

	if flask.request.method == "POST":
		data = flask.request.form
		save_user(
			id = id,
		    name = data.get("name"),
		    username = data.get("username"),
		    password = data.get("password")
			)
		return flask.redirect('/user')


@blueprint.route('/user_group/edit', methods=['GET', 'POST'])
def user_group_edit():
	id = flask.request.args.get('id', default = None, type = int)
	user_id = flask.request.args.get('user_id', default = None, type = int)

	if flask.request.method == "GET":
		return flask.render_template(
			'user_group_edit.html'
			, item_type = 'user_group'
			, user = search_object(user_id, User)
			, back_link = flask.request.referrer
			, groups = get_objects(Group)

			)

	if flask.request.method == "POST":
		data = flask.request.form
		save_object('user_group', id, data)
		return flask.redirect('/user/user_group/edit?user_id=' + str(user_id))