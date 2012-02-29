import ConfigParser
from lib import FGEucaMetricsDB
import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", dest="table_name", required=True,
			help="table name to delete")
	parser.add_argument("-d", dest="db_name", required=True,
			help="db name")
	parser.add_argument("-w", dest="where_clause",
			help="WHERE clauses")
	args = parser.parse_args()

	eucadb = FGEucaMetricsDB("futuregrid.cfg.local") 
	eucadb.change_table(args.table_name)

	# where_clause need to be query dict type 
	query_dict=""
	ret = eucadb.delete(query_dict)

if __name__ == '__main__':
	main()