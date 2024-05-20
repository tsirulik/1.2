# программа выборки сотрудников
import sqlite3

# выборка данных из таблицы сотрудников
conn = sqlite3.connect('company_projects.db')
cur = conn.cursor()

cur.execute('select * from employees')
rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()