from services.select_user_data import select_user_data
from services.save_services import insert_user_data
from data.source import DataView
from data.db_session import global_init
import argparse
from services.query_services import run_query


parser=argparse.ArgumentParser()

parser.add_argument('--query', help='Do the bar option')
parser.add_argument('--out', help='Foo the program')

args=parser.parse_args()



###init connection
global_init()


for id in args.query.split(","):
	run_query(int(id), args.out)