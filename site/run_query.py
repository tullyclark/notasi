from services.select_user_data import select_user_data
from services.save_services import insert_user_data
from data.source import DataView
from data.db_session import global_init, create_session
import argparse
import sys


parser=argparse.ArgumentParser()

parser.add_argument('--query', help='Do the bar option')
parser.add_argument('--out', help='Foo the program')

args=parser.parse_args()



###init connection
global_init()

session = create_session()

##get linked sessions
def run_query(id, out):
	views = session.query(DataView) \
	.filter_by(query_id=id) \
	.all()

	session.close()

	try:
		data = select_user_data(id)
	except Exception as error:
		print(str(error))

	if out == 'write':
		for d in data:
			for data_view in views:
				insert_user_data(d, data_view.id)
	else:
		print(data)


for id in args.query.split(","):
	run_query(int(id), args.out)