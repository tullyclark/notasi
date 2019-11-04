import flask
import pandas
from flask_login import login_required
from data.source import User, Group
from services.select_services import get_objects, search_object
from werkzeug.security import generate_password_hash
from services.save_services import save_object
import data.db_session as db_session
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


	session = db_session.create_session()
	try:
		users = get_objects(User, session)
	except Exception as error:
		print(str(error))
	finally:
		session.close()

	return flask.render_template(
		'user/index.html',
		users = users
	)

@blueprint.route('/edit', methods=['POST', 'GET'])
def reset():
	id = flask.request.args.get('id', default = None, type = int)

	if flask.request.method == "GET":

		session = db_session.create_session()
		try:
			data_obj = search_object(id, User, session)
		except Exception as error:
			print(str(error))
		finally:
			session.close()


		return flask.render_template(
			'user/edit_user.html'
			, item_type = 'user'
			, data_obj = data_obj
			, back_link = flask.request.referrer
		)

	if flask.request.method == "POST":
		data = flask.request.form
		session = db_session.create_session()
		try:
			save_object('user', id, data, session)
			session.commit()
		except Exception as error:
			print(str(error))
		finally:
			session.close()

		return flask.redirect('/user')


@blueprint.route('/user_group/edit', methods=['GET', 'POST'])
def user_group_edit():
	id = flask.request.args.get('id', default = None, type = int)
	user_id = flask.request.args.get('user_id', default = None, type = int)

	if flask.request.method == "GET":

		session = db_session.create_session()
		try:
			user = search_object(user_id, User, session)
			groups = get_objects(Group, session)
		except Exception as error:
			print(str(error))
		finally:
			session.close()

		return flask.render_template(
			'user_group_edit.html'
			, item_type = 'user_group'
			, user = user
			, back_link = flask.request.referrer
			, groups = groups
			)

	if flask.request.method == "POST":
		data = flask.request.form
		session = db_session.create_session()
		try:
			save_object('user_group', id, data, session)
			session.commit()
		except Exception as error:
			print(str(error))
		finally:
			session.close()
		return flask.redirect('/user/user_group/edit?user_id=' + str(user_id))