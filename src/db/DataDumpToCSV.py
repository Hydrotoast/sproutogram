import csv
import sqlite3

from operator import itemgetter

def main():
	with sqlite3.connect('extractions.db') as conn:
		cur = conn.cursor()
		cur.execute('SELECT DISTINCT method FROM feature')
		methods = [m[0] for m in cur.fetchall()]
		data = []
		for method in methods:
			cur.execute("SELECT sprout_count, branching_count \
				FROM feature \
				WHERE method = ? \
				ORDER BY filename",
				[method])
			row = cur.fetchall()
			data.append(row)
		with open('sprout_data.csv', 'w') as fh:
			writer = csv.writer(fh)
			for i, method in enumerate(methods):
				writer.writerow([method] +
					list(map(itemgetter(0), data[i])))

		with open('branching_data.csv', 'w') as fh:
			writer = csv.writer(fh)
			writer.writerow(methods)
			for i, method in enumerate(methods):
				writer.writerow([method] + list(map(itemgetter(1), data[i])))

main()
