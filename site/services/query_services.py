from services.select_user_data import select_user_data
from services.save_services import insert_user_data
from data.source import DataView
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
		for d in data:
			for data_view in views:
				insert_user_data(d, data_view.id)
	else:
		return(data)