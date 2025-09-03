import sqlite3

conn = sqlite3.connect('shop.db')

curr = conn.cursor()

def write(table_name, data):
    for dt in data:
        s = f'insert into {table_name} values('
        for d in dt:
            if not isinstance(d, str):
                s += f'{d},'
            else:
                s += f'\"{d}\",'
        s = s[:-1]
        s += ')'
        curr.execute(s)

rows = curr.execute('select * from Customer')

orders = rows.fetchall()

for o in orders:
    print(o)

conn.commit()
curr.close()
conn.close()