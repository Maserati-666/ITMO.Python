import sys
from PyQt5.QtWidgets import QApplication

from Model.AirportsModel import AirportsModel
from Controller.Controller import AirportController

def main():
    app = QApplication(sys.argv)

    # создаём модель
    model = AirportsModel()

    # создаём контроллер и передаём ему ссылку на модель
    controller = AirportController(model)

    app.exec()


if __name__ == '__main__':
    sys.exit(main())