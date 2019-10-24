from services.select_user_data import select_user_data
from services.save_services import insert_user_data
from data.source import DataView, ViewRun
from data.db_session import create_session

##get linked sessions
def run_query(id, out):
	session = create_session()
	views = session.query(DataView) \
	.filter_by(query_id=id) \
	.all()

	session.close()

	data=[]
	try:
		data = select_user_data(id)
	except Exception as error:
		print(str(error))

	if out == 'write':
		for data_view in views:

			session = create_session()

			view_run = ViewRun()
			session.add(view_run)
			view_run.data_view_id = data_view.id
			session.commit()

			for d in data:
				insert_user_data(d, view_run.id)
			
			session.close()
	else:
		return(data)