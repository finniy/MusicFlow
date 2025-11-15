from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import pyqtSignal

from app.windows.main_window import MainWindow
from app.database.cruds.users_crud import create_user, get_user_by_username
from app.database.session import session_local
from app.utils.security import hash_password
from app.utils.validators import is_valid_password, is_valid_username


class RegisterWindow(QWidget):
    back_to_login = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self) -> None:
        import os

        # Поиск UI файла
        ui_paths = [
            "ui/register_window.ui",
            "../ui/register_window.ui"
        ]

        for ui_path in ui_paths:
            if os.path.exists(ui_path):
                uic.loadUi(ui_path, self)
                break
        else:
            raise FileNotFoundError("Не найден файл register_window.ui")

        self.setWindowTitle("MusicFlow — Регистрация")
        self.register_button.clicked.connect(self.handle_register)
        self.go_to_login.clicked.connect(self.handle_go_login)

    def handle_register(self) -> None:
        """
        Обрабатывает регистрацию нового пользователя.
        """
        username = self.login_table.text().strip()
        password = self.password_table.text().strip()

        self.login_table.clear()
        self.password_table.clear()

        if not is_valid_username(username) or not is_valid_password(password):
            QMessageBox.warning(self, "Ошибка", "Невалидные данные")
            return

        with session_local() as db:
            existing_user = get_user_by_username(db, username)
            if existing_user:
                QMessageBox.warning(self, "Ошибка", "Имя пользователя уже занято")
                return

            hashed = hash_password(password)
            new_user = create_user(db, username, hashed)
            QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")

            self.main_window = MainWindow(current_user_id=new_user.id)
            self.main_window.show()
            self.close()

    def handle_go_login(self) -> None:
        """
        Возвращает пользователя к окну входа.
        """
        self.close()
        self.back_to_login.emit()
