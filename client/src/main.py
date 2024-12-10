from PyQt5.QtWidgets import QApplication
from TableRecogniser import TableRecogniser
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableRecogniser()
    window.show()
    sys.exit(app.exec())
