import sqlite3

data = []
data.append(('Ang1 250 ng_ml 1 Day 7', 14, 8, 2))
data.append(('1k 3 Day 7', 23, 14, 3))
data.append(('1k 2 Day 7', 15, 11, 4))
data.append(('10k 5 Day 7', 20, 10, 4))
data.append(('10k 1 Day 7', 16, 7, 0))
data.append(('Control 5 Day 7', 17, 7, 2))
data.append(('Control 4 Day 7', 17, 8, 3))
data.append(('Control 2 Day 7', 18, 12, 7))
data.append(('Control 1 Day 7', 17, 10, 2))
data.append(('20k 5 Day 7', 24, 9, 4))
data.append(('20k 3 Day 7', 12, 6, 11))
data.append(('20k 2 Day 7', 23, 15, 3))
data.append(('20k 1 Day 7', 17, 10, 0))
data.append(('Ang1 100ng_ml 5 Day 7', 13, 9, 3))
data.append(('Ang1 100ng_ml 3 Day 7', 12, 7, 1))

with sqlite3.connect('extractions.db') as conn:
	cur = conn.cursor()
	cur.executemany('INSERT INTO training VALUES (?, ?, ?, ?)', data)
