import requests
from bs4 import BeautifulSoup
import sqlite3

# Функция для парсинга страницы
def parse_page():
    url = 'https://ru.wikipedia.org/wiki/Список_самых_дорогих_картин'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    response = requests.get(url, timeout=180)

    # Находим таблицу с данными
    table = soup.find('table', {'class': 'wikitable sortable'})

    # Инициализируем списки для хранения данных
    paintings = []
    artists = []
    sale_locations = []

    # Проходим по строкам таблицы
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        cells = row.find_all('a')

        # Извлекаем данные из ячеек
        painting = cells[1].text.strip()
        artist = cells[2].text.strip()
        sale_location = cells[3].text.strip()
        price = float(cells[4].text.strip().replace(' $', '').replace(',', ''))

        # Добавляем данные в списки
        paintings.append((painting, price))
        artists.append(artist)
        sale_locations.append(sale_location)

    return paintings, artists, sale_locations

# Создание базы данных и заполнение таблиц
def create_database():
    conn = sqlite3.connect('art_database.db')
    c = conn.cursor()

    # Создание таблиц
    c.execute('''CREATE TABLE IF NOT EXISTS paintings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS artists
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sale_locations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')

    # Получение данных из парсера
    paintings, artists, sale_locations = parse_page()

    # Заполнение таблиц
    for painting, price in paintings:
        c.execute("INSERT INTO paintings (name, price) VALUES (?, ?)", (painting, price))

    for artist in set(artists):
        c.execute("INSERT INTO artists (name) VALUES (?)", (artist,))

    for location in set(sale_locations):
        c.execute("INSERT INTO sale_locations (name) VALUES (?)", (location,))

    conn.commit()
    conn.close()

# Вызов функции для создания базы данных
create_database()

# Функция для выполнения запросов к базе данных
def execute_query(query, *args):
    conn = sqlite3.connect('art_database.db')
    c = conn.cursor()
    c.execute(query, args)
    result = c.fetchall()
    conn.close()
    return result

# Топ N художников по числу картин
def top_artists_by_paintings(N):
    query = """
        SELECT a.name, COUNT(*) as num_paintings
        FROM artists a
        JOIN paintings p ON a.name = p.name
        GROUP BY a.name
        ORDER BY num_paintings DESC
        LIMIT ?
    """
    return execute_query(query, N)

# Топ N художников по цене картин
def top_artists_by_price(N):
    query = """
        SELECT a.name, SUM(p.price) as total_price
        FROM artists a
        JOIN paintings p ON a.name = p.name
        GROUP BY a.name
        ORDER BY total_price DESC
        LIMIT ?
    """
    return execute_query(query, N)

# Самые дорогие картины по годам
def most_expensive_paintings_by_year():
    query = """
        SELECT p.name, p.price, strftime('%Y', p.name) as year
        FROM paintings p
        ORDER BY p.price DESC
    """
    return execute_query(query)

# Суммарная стоимость топ N самых дорогих картин
def total_value_of_top_paintings(N):
    query = """
        SELECT SUM(p.price) as total_value
        FROM (
            SELECT p.name, p.price
            FROM paintings p
            ORDER BY p.price DESC
            LIMIT ?
        ) p
    """
    return execute_query(query, N)


print("Топ 5 художников по числу картин:")
for artist, num_paintings in top_artists_by_paintings(5):
    print(f"{artist}: {num_paintings} картин")

print("\nТоп 3 художников по цене картин:")
for artist, total_price in top_artists_by_price(3):
    print(f"{artist}: ${total_price:.2f}")

print("\nСамые дорогие картины по годам:")
for painting, price, year in most_expensive_paintings_by_year():
    print(f"{painting} ({year}): ${price:.2f}")

print("\nСуммарная стоимость топ 10 самых дорогих картин:")
total_value = total_value_of_top_paintings(10)[0][0]
print(f"${total_value:.2f}")
