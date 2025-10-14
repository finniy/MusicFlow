from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from app.utils.security import verify_password
from app.database.cruds.users_crud import get_user_by_username
from app.database.session import session_local
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
        username = self.login_table.text().strip()
        password = self.password_table.text().strip()

        # Очищаем поля
        self.login_table.setText("")
        self.password_table.setText("")

        # Проверка на пустые поля
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        try:
            with session_local() as db:
                user = get_user_by_username(db, username)
        except:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return

        if user is None:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return

        if not verify_password(password, user.password):
            QMessageBox.warning(self, "Ошибка", "Неверный пароль")
            return

        print(f"Успешный вход: {username}")

    def handle_register(self):
        print("Переход к окну регистрации")


def main():
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())
