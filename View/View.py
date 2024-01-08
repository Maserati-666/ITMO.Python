from PyQt5.QtWidgets import QMainWindow

from View.MainWindow import Ui_MainWindow

class AirportView(QMainWindow):
    """
    Класс отвечающий за визуальное представление AirportModel.
    """

    def __init__(self, inController, inModel, parent=None):
        """
        Конструктор принимает ссылки на модель и контроллер.
        """
        super(QMainWindow, self).__init__(parent)
        self.mController = inController
        self.mModel = inModel

        # подключаем визуальное представление
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # связываем изменения комбобокс с контроллером
        self.ui.comboBox.addItems(self.mModel.countries)
        self.ui.comboBox.currentTextChanged.connect(self.mController.create_list_cities)

        # связываем нажатие кнопки с контроллером
        self.ui.pushButton.clicked.connect(self.mController.buttonClick)

    # Метод для обновления данных в comboBox_2 после изменений в comboBox
    def updateCombobox2(self):
        self.ui.comboBox_2.clear()
        self.ui.comboBox_2.addItems(self.mModel.cities_airports)
