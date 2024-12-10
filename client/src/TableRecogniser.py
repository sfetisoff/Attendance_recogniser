from PyQt5.QtWidgets import QMainWindow
from MainWindowDesign import Ui_MainWindow
import client


class TableRecogniser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Подключаем и создаем главное окно
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.UiComponents()

    def UiComponents(self):
        self.ui.recogniseButton.clicked.connect(client.recognise_photo)
        self.ui.resultButton.clicked.connect(self.result)
        self.ui.loadToServButton.clicked.connect(client.upload_file_table)

    def result(self):
        client.get_file_table('table.xlsx'),
        client.start_excel()
