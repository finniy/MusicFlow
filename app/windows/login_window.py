import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox

from app.windows.register_window import RegisterWindow
from app.database.cruds.users_crud import get_user_by_username
from app.database.session import session_local
from app.utils.security import verify_password
from app.utils.validators import is_valid_password, is_valid_username


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("ui/login_window.ui", self)
        self.setWindowTitle("MusicFlow — Авторизация")

        self.login_button.clicked.connect(self.handle_login)
        self.go_to_register.clicked.connect(self.open_register_window)

    def handle_login(self):
        username = self.login_table.text().strip()
        password = self.password_table.text().strip()

        self.login_table.clear()
        self.password_table.clear()

        if not is_valid_username(username) or not is_valid_password(password):
            QMessageBox.warning(self, "Ошибка", "Невалидные данные")
            return

        try:
            with session_local() as db:
                user = get_user_by_username(db, username)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            print(f"Ошибка при обращении к базе данных: {e}")
            return

        if user is None or not verify_password(password, user.password):
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return

        print(f"Успешный вход: {username}")

    def open_register_window(self):
        self.hide()
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.register_window.back_to_login.connect(self.show_again)

    def show_again(self):
        self.show()


def main():
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())
