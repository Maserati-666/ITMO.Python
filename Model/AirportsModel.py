# Класс AirportsModel содержит данные о странах, городах в выбранной стране,
# и аэропортах в выбранном городе, а также расположении файла базы данных,
# содержит сеттеры и геттеры для обращения к полям модели
class AirportsModel:
    def __init__(self):
        self._countries = []          # Содержит список стран из базы данных
        self._cities = []             # Содержит список городов в выбранной стране
        self._cities_airports = []    # Содержит список город-аэропорт в выбранном городе
        self._airports = []           # Содержит список аэропортов в выбранном городе
        self._country = ""          # Содержит выбранную страну
        self._city = ""             # Содержит выбранный город
        self._airport = ""          # Содержит выбранный аэропорт
        self._path_file = ""        # Содержит путь до файла базы данных

    @property
    def countries(self):
        return self._countries

    @countries.setter
    def countries(self, countries):
        self._countries = countries

    @property
    def cities(self):
        return self._cities

    @cities.setter
    def cities(self, cities):
        self._cities = cities

    @property
    def cities_airports(self):
        return self._cities_airports

    @cities_airports.setter
    def cities_airports(self, cities_airports):
        self._cities_airports = cities_airports

    @property
    def airports(self):
        return self._airports

    @airports.setter
    def airports(self, airports):
        self._airports = airports

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, country):
        self._country = country

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, city):
        self._city = city

    @property
    def airport(self):
        return self._airport

    @airport.setter
    def airport(self, airport):
        self._airport = airport
