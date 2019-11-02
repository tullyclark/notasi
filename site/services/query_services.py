from services.select_user_data import select_user_data
from services.save_services import insert_user_data
from data.source import DataView, ViewRun
from data.db_session import create_session

##get linked sessions
def run_query(id, out):
	session = create_session()
	data=[]

	try:
		views = session.query(DataView).filter_by(query_id=id).all()
		data = select_user_data(id, session)
		
		if out == 'write':
			for data_view in views:

				view_run = ViewRun()
				session.add(view_run)
				view_run.data_view_id = data_view.id

				for d in data:
					insert_user_data(d, view_run.id, session)
		session.commit()


	except Exception as error:
		print(str(error))
		# session.rollback()
	finally:
		session.close()
		return(data)