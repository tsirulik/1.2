from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pypika import Query, Table, Parameter

import sqlite3

# Создаем экземпляр драйвера Selenium
driver = webdriver.Chrome()

# Открываем страницу
driver.get(
    "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B5%D0%B9_%D0%B8_%D0%B0%D0%BA%D1%82%D1%91%D1%80%D0%BE%D0%B2_%D0%9A%D0%B8%D0%BD%D0%B5%D0%BC%D0%B0%D1%82%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B9_%D0%B2%D1%81%D0%B5%D0%BB%D0%B5%D0%BD%D0%BD%D0%BE%D0%B9_Marvel_(%D0%A1%D0%B0%D0%B3%D0%B0_%D0%91%D0%B5%D1%81%D0%BA%D0%BE%D0%BD%D0%B5%D1%87%D0%BD%D0%BE%D1%81%D1%82%D0%B8)")

# Ждем загрузки таблицы
wait = WebDriverWait(driver, 10)
table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.wikitable")))

# Извлекаем данные из таблицы
data = []
for row in table.find_elements(By.TAG_NAME, "tr")[1:]:
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) == 5:
        title = cells[0].text.strip()
        director = cells[1].text.strip()
        # Проверяем, является ли ячейка с годом числом
        try:
            year = int(cells[2].text.strip())
        except ValueError:
            continue  # Пропускаем строку, если значение в ячейке не является числом
        try:
            gross = float(cells[3].text.strip().replace(",", ""))
        except ValueError:
            continue  # Пропускаем строку, если значение в ячейке не является числом
        rank = int(cells[4].text.strip())
        data.append((title, director, year, gross, rank))

# Закрываем браузер
driver.quit()

# Создаем подключение к базе данных SQLite
conn = sqlite3.connect("marvel_films.db")
c = conn.cursor()

# Создаем таблицы
c.execute("""CREATE TABLE IF NOT EXISTS films (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT,
             director TEXT,
             year INTEGER,
             gross REAL,
             rank INTEGER
         )""")

c.execute("""CREATE TABLE IF NOT EXISTS directors (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT
         )""")

# Заполняем таблицу films
for title, director, year, gross, rank in data:
    c.execute("INSERT INTO films (title, director, year, gross, rank) VALUES (:title, :director, :year, :gross, :rank)",
              {"title": title, "director": director, "year": year, "gross": gross, "rank": rank})

# Заполняем таблицу directors
directors = set(row[1] for row in data)
for director in directors:
    c.execute("INSERT INTO directors (name) VALUES (:name)", {"name": director})

conn.commit()
conn.close()

# Создаем объекты таблиц
films = Table("films")
directors = Table("directors")

# Два запроса с JOIN
query1 = (
    Query.from_(films)
        .join(directors, how=films.director == directors.name)
        .select(films.title, directors.name)
)
query2 = (
    Query.from_(films)
        .join(directors, how=films.director == directors.name)
        .where(films.year > 2010)
        .select(films.title, films.year, directors.name)
)

# Три запроса с расчетом статистики/группировкой/агрегирующими функциями
query3 = Query.from_(films).select(films.year, Query.avg(films.gross).as_("avg_gross"))
query4 = Query.from_(films).groupby(films.director).select(films.director, Query.count(films.id).as_("num_films"))
query5 = Query.from_(films).where(films.year >= 2015).select(films.year, Query.sum(films.gross).as_("total_gross"))
