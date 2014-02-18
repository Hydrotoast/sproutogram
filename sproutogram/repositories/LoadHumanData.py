import sqlite3


def main():
    data = []
    data.append(('Ang1 250 ng_ml 1 Day 7', 14, 8, 2, 11))
    data.append(('1k 3 Day 7', 23, 14, 3, 14))
    data.append(('1k 2 Day 7', 15, 11, 4, 14))
    data.append(('10k 5 Day 7', 20, 10, 4, 16))
    data.append(('10k 1 Day 7', 16, 7, 0, 13))
    data.append(('Control 5 Day 7', 17, 7, 2, 26))
    data.append(('Control 4 Day 7', 17, 8, 3, 10))
    data.append(('Control 2 Day 7', 18, 12, 7, 11))
    data.append(('Control 1 Day 7', 17, 10, 2, 10))
    data.append(('20k 5 Day 7', 24, 9, 4, 9))
    data.append(('20k 3 Day 7', 12, 6, 11, 9))
    data.append(('20k 2 Day 7', 23, 15, 3, 17))
    data.append(('20k 1 Day 7', 17, 10, 0, 15))
    data.append(('Ang1 100ng_ml 5 Day 7', 13, 9, 3, 10))
    data.append(('Ang1 100ng_ml 3 Day 7', 12, 7, 1, 7))


    with sqlite3.connect('extractions.repositories') as conn:
        cur = conn.cursor()
        cur.executemany('INSERT INTO training VALUES (?, ?, ?, ?, ?)', data)

if __name__ == '__main__':
    main()
