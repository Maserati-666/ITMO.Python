import os
import sqlite3
import json
from View.View import AirportView

class AirportController():

    def __init__(self, inModel):
        """
                Конструктор принимает ссылку на модель.
                Конструктор создаёт и отображает представление.
        """
        self.mModel = inModel
        self.create_DB()
        self.create_list_countries()
        self.mView = AirportView(self, self.mModel)
        self.mView.show()

    # Метод для создания файла базы данных SQLite
    def create_DB(self):
        path_fileDB = r'C:\Users\ASER\Desktop\Project\AirportPyQT5\Utility\airports.db' # выбор директории куда будет создан файл DB.
        self.mModel.path_file = path_fileDB
        path_file_json = r'C:\Users\ASER\Desktop\Project\AirportPyQT5\Utility\airports.json' # выбор директории где лежит json
        if os.path.isfile(path_fileDB):
            print('Файл найден')
        else:
            conn = self.connect_DB()
            cur = conn.cursor()
            '''
            3. Создание таблицы Airports
            '''
            cur.execute("""CREATE TABLE IF NOT EXISTS airports(
               id INT PRIMARY KEY,
               airport TEXT,
               city_id INT,
               country_id INT,
               iata TEXT,
               icao TEXT,
               latitude FLOAT,
               longitude FLOAT,
               elevation INT,
               utc INT,
               dst TEXT,
               region TEXT);
            """)
            conn.commit()  # Сохраняет изменения для объекта соединения
            '''
            4. Создание таблицы cities
            '''
            cur.execute("""CREATE TABLE IF NOT EXISTS cities(
               city_id INT PRIMARY KEY,
               city TEXT,
               id_country INT NOT NULL);
            """)
            '''
            5. Создание таблицы countries
            '''
            cur.execute("""CREATE TABLE IF NOT EXISTS countries(
               id INT PRIMARY KEY,
               country TEXT);
            """)
            '''
            6. Экспорт данных из json-файла и добавление данных в базу данных
            '''
            with open(path_file_json, 'r') as data:
                airports = json.load(data)
                columns = ['id', 'airport', 'city', 'country', 'iata', 'icao', 'latitude', 'longitude', 'elevation',
                           'utc', 'dst',
                           'region']
                countries = []
                cities = []
                table = []
                citi = []
                countri = []
                count_city = 0
                count_country = 0
                for row in airports:
                    for elem in columns:
                        if elem == 'city':
                            if row['city'] not in cities or row['country'] not in countries:
                                cities.append(row['city'])
                                count_city += 1
                                table.append(cities.index(row['city']) + 1)
                                citi.append(count_city)
                                citi.append(row['city'])
                                if row['country'] not in countries:
                                    countries.append(row['country'])
                                    count_country += 1
                                    countri.append(count_country)
                                    countri.append(row['country'])
                                    cur.execute("""INSERT INTO countries values(?, ?)""", countri)
                                    countri = []
                                citi.append(countries.index(row['country']) + 1)
                                cur.execute("""INSERT INTO cities values(?, ?, ?)""", citi)
                                citi = []
                            else:
                                table.append(cities.index(row['city']) + 1)
                        elif elem == 'country':
                            table.append(countries.index(row['country']) + 1)
                        else:
                            table.append(row[elem])
                    print(table)
                    cur.execute("""INSERT INTO airports values(?,?,?,?,?,?,?,?,?,?,?,?)""", table)
                    print(f'{row["id"]} data inserted Succefully')
                    table = []
            conn.commit()
            conn.close()

    # Метод для подключения к базе данных SQLite
    def connect_DB(self):
        path_file = self.mModel.path_file # выбор директории куда будет создан файл DB.
        '''
            1. Функция connect() создает соединение с базой данных SQLite и возвращает объект, представляющий ее.
        '''
        conn = sqlite3.connect(path_file)  # Создает объект connection, а также новый файл airports.db в рабочей директории
        return conn

    # Метод для подключения к базе данных SQLite
    def create_list_countries(self):
        conn = self.connect_DB()
        cur = conn.cursor()
        cur.execute("SELECT country FROM countries ORDER BY country ASC")
        result1 = cur.fetchall()
        result2 = [row[0] for row in result1]
        list_for_combo1 = ['--Выберите страну--'] + result2
        conn.commit()
        conn.close()
        self.mModel.countries = list_for_combo1

    # Метод для создания списка для comboBox_2
    def create_list_cities(self):
        self.mModel.country = self.mView.ui.comboBox.currentText()
        conn = self.connect_DB()
        cur = conn.cursor()
        cur.execute("SELECT id FROM countries WHERE country = ?", (self.mModel.country,))
        result1 = cur.fetchall()
        cur.execute("SELECT city, airport FROM airports JOIN cities ON airports.city_id=cities.city_id"
                        " WHERE country_id = ? ORDER BY city ASC", result1.pop(0))
        result2 = cur.fetchall()
        list_1 = [row[0] + " - " + row[1] for row in result2]
        list_2 = [row[0] for row in result2]
        list_3 = [row[1] for row in result2]
        self.mModel.cities = list_2
        self.mModel.airports = list_3
        list_for_combo2 = []
        counter = -1
        for i in list_2:
            counter += 1
            if list_2.count(i) > 1:
                list_for_combo2.append(list_1[counter])
            else:
                list_for_combo2.append(list_2[counter])
        conn.commit()
        conn.close()
        self.mModel.cities_airports = list_for_combo2
        self.mView.updateCombobox2()

    # Метод для обработчика события нажатия на кнопку "Показать на карте"
    def buttonClick(self):
        self.mView.ui.browser.setHtml(self.html_page())

    # Метод для использования API Google Maps (создание html-страницы)
    def html_page(self):
        api_key = ''
        a1 = self.mModel.country
        if a1 == '':
            html_page = ''' <body>
                            <header>
                            <h1>Пожалуйста выберите страну!!!</h1>
                            </header>
                            </body>
                        '''
            return html_page
        else:
            a2 = self.mView.ui.comboBox_2.currentText()
            conn = self.connect_DB()
            cur = conn.cursor()
            if a2.count(' - ') == 0:
                cur.execute("SELECT airport FROM airports JOIN cities ON airports.city_id=cities.city_id"
                            " JOIN countries ON airports.country_id=countries.id"
                            " WHERE country = ? AND city = ?", (str(a1), str(a2)))
                a3 = cur.fetchone()
                self.mModel.city = a2
                self.mModel.airport = a3[0]
                conn.commit()
            else:
                for val in self.mModel.cities:
                    if a2.count(val) == 1:
                        self.mModel.city = val
                for val in self.mModel.airports:
                    if a2.count(val) == 1:
                        self.mModel.airport = val
            z2 = (self.mModel.airport.replace(' ', '+') + ',' + self.mModel.city.replace(' ', '+') + ','
                  + self.mModel.country.replace(' ', '+'))
            conn.commit()
            conn.close()
            z1 = '''<iframe
                                  width="100%"
                                  height="100%"
                                  frameborder="1" style="border:1"
                                  referrerpolicy="no-referrer-when-downgrade"
                                  src="https://www.google.com/maps/embed/v1/place?key=''' + api_key + '&q='
            z3 = '''&zoom=14"
                          allowfullscreen>
                        </iframe>
                        '''
            html_page = z1 + z2 + z3
            return html_page
