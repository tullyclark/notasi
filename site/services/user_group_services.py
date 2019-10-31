
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

			for group in set([d["group_name"] for d in notasi_query if d['group_category'] == group_category]):

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

				

	return []

def update_user_groups(
	query
):	
	session = db_session.create_session()
		
	if query.notasi_query:
		notasi_query = pandas.read_sql(query.notasi_query, db_session.notasi_engine()).to_dict('records')
		group_categories = []
		

		for row in notasi_query:
			
			if row["group_category"] and row["group_category"] not in group_categories:
				group_categories.append(row["group_category"])


			existing_row = session.query(UserGroup) \
					.join(Group) \
					.join(GroupCategory) \
					.join(User) \
					.filter(Group.name==row["group_name"]) \
					.filter(GroupCategory.name==row["group_category"]) \
					.filter(User.username==row["username"]) \
					.first()

			existing_group = session.query(Group).filter(GroupCategory.name==row["group_category"]).filter(Group.name==row["group_name"]).first()
			existing_user = session.query(User).filter(User.username==row["username"]).first()

			if not existing_row and existing_group and existing_user:
				new_row = UserGroup()
				session.add(new_row)
				new_row.group_id = existing_group.id
				new_row.user_id = existing_user.id
				session.commit()

		for group_category in group_categories:
			existing_rows = session.query(UserGroup) \
					.join(Group) \
					.join(GroupCategory) \
					.join(User) \
					.filter(GroupCategory.name==row["group_category"]) \
					.all()
			for existing_row in existing_rows:
				if {"username": existing_row.user.username
					, "group_category": existing_row.group.group_category.name
					, "group_name": existing_row.group.name} not in notasi_query:

					session.delete(existing_row)
					session.commit()





	session.close()
	return []








			