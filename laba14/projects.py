# программа выборки проектов
import sqlite3

# выборка данных из таблицы проектов
conn = sqlite3.connect('company_projects.db')
cur = conn.cursor()

cur.execute('select * from projects')
rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()
