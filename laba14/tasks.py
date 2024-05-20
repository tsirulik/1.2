# программа выборки задач
import sqlite3

# выборка данных из таблицы задач
conn = sqlite3.connect('company_projects.db')
cur = conn.cursor()

cur.execute('select * from tasks')
rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()
