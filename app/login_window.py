from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget
import sys


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("ui/login_window.ui", self)
        self.setWindowTitle("MusicFlow — Авторизация")

        self.login_button.clicked.connect(self.handle_login)
        self.go_to_register.clicked.connect(self.handle_register)

    def handle_login(self):
        username = self.login_table.text()
        password = self.password_table.text()

        self.login_table.setText("")
        self.password_table.setText("")

        print(f"Пытаемся войти: {username=} {password=}")

    def handle_register(self):
        print("Переход к окну регистрации")


def main():
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())
