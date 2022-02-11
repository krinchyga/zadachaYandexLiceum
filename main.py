import sys, os, requests

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

URL = "http://static-maps.yandex.ru/1.x"

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.scale = 0
        self.longitude = 0
        self.latitude = 0

    def initUI(self):
        self.setGeometry(300, 300, 400, 425)
        self.setWindowTitle('Часть 1')

        self.btn = QPushButton('Сформировать карту', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(100, 100)
        self.btn.clicked.connect(self.getScale)

        self.label = QLabel(self)
        self.label.setText("Укажите координаты")
        self.label.move(20, 10)

        self.name_label = QLabel(self)
        self.name_label.setText("Укажите масштаб")
        self.name_label.move(20, 70)

        self.longitude_edit = QLineEdit(self)
        self.longitude_edit.move(170, 10)
        self.latitude_edit = QLineEdit(self)
        self.latitude_edit.move(170, 30)
        self.scale_edit = QLineEdit(self)
        self.scale_edit.move(170, 70)

        self.image = QLabel(self)
        self.image.move(0, 125)
        self.image.resize(400, 300)

    def getScale(self):
        self.scale = float(self.scale_edit.text())
        self.longitude = float(self.longitude_edit.text())
        self.latitude = float(self.latitude_edit.text())
        self.getImage()

    def getImage(self):
        params = {
            "ll": f"{self.longitude},{self.latitude}",
            "spn": f"{self.scale},{self.scale}",
            "l": "map",
            "size": "400,300"
        }
        response = requests.get(URL, params=params)
        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def mousePressEvent(self, event):
        self.scale_edit.setEnabled(True)
        self.longitude_edit.setEnabled(True)
        self.latitude_edit.setEnabled(True)

    def keyPressEvent(self, event):
        self.scale_edit.setEnabled(False)
        self.longitude_edit.setEnabled(False)
        self.latitude_edit.setEnabled(False)
        self.image.setFocus()
        if event.key() == Qt.Key_PageUp and self.scale + 0.3 < 3:
            self.scale = round(self.scale + 0.3, 4)
        if event.key() == Qt.Key_PageDown and self.scale - 0.3 > 0:
            self.scale = round(self.scale - 0.3, 4)
        if event.key() == Qt.Key_Right and self.longitude - 0.3 > 0:
            self.longitude = round(self.longitude - 0.3, 6)
        if event.key() == Qt.Key_Left and self.longitude + 0.3 < 180:
            self.longitude = round(self.longitude + 0.3, 6)
        if event.key() == Qt.Key_Up and self.latitude - 0.03 > 0:
            self.latitude = round(self.latitude - 0.03, 6)
        if event.key() == Qt.Key_Down and self.latitude + 0.03 < 180:
            self.latitude = round(self.latitude + 0.03, 6)
        self.getImage()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())