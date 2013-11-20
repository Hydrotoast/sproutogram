import math
import sqlite3 as sqlite

def main():
	with sqlite.connect('extractions.db') as conn:
		cur = conn.cursor()
		cur.execute('SELECT * FROM overview')
		rows = cur.fetchall()
		for row in rows:
			print '{0:s}, {1:.2f}, {2:.2f}'.format(row[0], math.sqrt(row[1]), math.sqrt(row[2]))

if __name__ == '__main__':
	main()
