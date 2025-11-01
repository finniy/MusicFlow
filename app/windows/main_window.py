from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem, QFileDialog
from app.database.session import session_local
from app.database.cruds.song_crud import get_all_songs, create_song
from app.database.cruds.favourite_crud import get_user_favourites
import sys
import random

class MainWindow(QMainWindow):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.initUI()

    def initUI(self):
        uic.loadUi("ui/main_window.ui", self)
        self.setWindowTitle("MusicFlow — Плеер")

        # --- Вкладка Рекомендации ---
        self.playRandomButton.clicked.connect(self.recommendation)
        with session_local() as db:
            self.recommendations = get_all_songs(db)

        # --- Вкладка Избранное ---
        self.playFavoriteButton.clicked.connect(self.play_favorite)
        self.load_favorites()

        # --- Вкладка Загрузка песен ---
        self.chooseAvatarButton.clicked.connect(self.choose_avatar)
        self.chooseFileButton.clicked.connect(self.choose_song_file)
        self.uploadButton.clicked.connect(self.upload_song)

    # ---------------- Рекомендации ----------------
    def recommendation(self):
        if self.recommendations:
            song = random.choice(self.recommendations)
            self.currentRecommendationLabel.setText(f"Сейчас играет: {song.title}")
            QMessageBox.information(self, "Рекомендация", f"Воспроизводим случайную песню: {song.title}")
        else:
            QMessageBox.warning(self, "Рекомендации", "Список рекомендаций пуст")

    # ---------------- Избранное ----------------
    def load_favorites(self):
        self.favoritesList.clear()
        with session_local() as db:
            favorites = get_user_favourites(db, CURRENT_USER_ID)
            for song in favorites:
                self.favoritesList.addItem(QListWidgetItem(song.title))

    def play_favorite(self):
        item = self.favoritesList.currentItem()
        if item:
            song = item.text()
            QMessageBox.information(self, "Избранное", f"Воспроизводим: {song}")
        else:
            QMessageBox.warning(self, "Избранное", "Выберите песню из списка")

    # ---------------- Загрузка песен ----------------
    def choose_avatar(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите аватар", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.avatarPathLabel.setText(path)

    def choose_song_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите песню", "", "Audio Files (*.mp3 *.wav *.ogg)")
        if path:
            self.filePathLabel.setText(path)

    def upload_song(self):
        song_name = self.songNameInput.text().strip()
        avatar_path = self.avatarPathLabel.text()
        song_path = self.filePathLabel.text()

        if not song_name or not avatar_path or not song_path:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        with session_local() as db:
            create_song(db, song_name, song_path, avatar_path)
            self.recommendations = get_all_songs(db)  # обновляем рекомендации
            self.load_favorites()  # обновляем избранное (если пользователь добавил себе песню)

        self.uploadStatus.setText(f"Песня '{song_name}' загружена!")
        QMessageBox.information(self, "Загрузка", f"Песня '{song_name}' успешно загружена")
        self.songNameInput.clear()
        self.avatarPathLabel.clear()
        self.filePathLabel.clear()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
