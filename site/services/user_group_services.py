
import pandas

import data.db_session as db_session
from data.source import User, GroupCategory,UserGroup, Group
from utils.json import flatten_json



def update_users(
	query
):

	if query.notasi_query:
		session = db_session.create_session()
		notasi_query = pandas.read_sql(query.notasi_query, db_session.notasi_engine()).to_dict('records')

		for row in notasi_query:
			user = session.query(User).filter_by(username=row["username"]).first()
			if user:
				if user.name !=row["name"]:
					user.name =row["name"]
			else:
				user = User()
				session.add(user)
				user.username = row["username"]
				user.name = row["name"]
			session.commit()
		session.close()


	response = [{"job":"users added"}]

	return flatten_json(response)

def update_groups(
	query
):

	session = db_session.create_session()
		
	if query.notasi_query:
		notasi_query = pandas.read_sql(query.notasi_query, db_session.notasi_engine()).to_dict('records')

		
		for group_category in set(d["group_category"] for d in notasi_query):
			category = session.query(GroupCategory).filter_by(name=group_category).first() 
			if not category:
				category = GroupCategory()
				session.add(category)
				category.name = group_category
				session.commit()

			for group in set([d["group"] for d in notasi_query if d['group_category'] == group_category]):

				stored_group = session.query(Group) \
					.join(GroupCategory) \
					.filter(Group.name==group) \
					.filter(GroupCategory.name==group_category) \
					.first() 

				if not stored_group:
					stored_group = Group()
					session.add(stored_group)
					stored_group.name = group
					stored_group.group_category_id = category.id
					session.commit()

				
				stored_rows = session.query(UserGroup) \
					.join(Group) \
					.join(GroupCategory) \
					.join(User) \
					.filter(Group.name==group) \
					.filter(GroupCategory.name==group_category) \
					.all()

				for row in stored_rows:
					if not [d for d in notasi_query if d['group_category'] == row.group.group_category.name \
						and d['group'] == row.group.name \
						and d['username'] == row.user.username]:
						session.delete(row)
						session.commit()

				for row in notasi_query:
					if not [d for d in stored_rows if d.user.username == row['username']]:
						user = session.query(User) \
							.filter(User.username==row['username']) \
							.first()
						new_user_group = UserGroup()
						session.add(new_user_group)
						new_user_group.group_id = stored_group.id
						new_user_group.user_id = user.id
						session.commit()
	return []






			