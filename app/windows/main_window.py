from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem, QFileDialog
import sys
import random

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("ui/main_window.ui", self)
        self.setWindowTitle("MusicFlow — Плеер")

        # Вкладка рекомендации
        self.playRandomButton.clicked.connect(self.recommendation)

        # Вкладка избранное
        self.playFavoriteButton.clicked.connect(self.play_favorite)

        # Вкладка загрузка
        self.chooseAvatarButton.clicked.connect(self.choose_avatar)
        self.chooseFileButton.clicked.connect(self.choose_song_file)
        self.uploadButton.clicked.connect(self.upload_song)

    # --- Рекомендации ---
    def recommendation(self):
        if self.recommendations: # тут бд
            song = random.choice(self.recommendations)
            self.currentRecommendationLabel.setText(f"Сейчас играет: {song}")
            QMessageBox.information(self, "Рекомендация", f"Воспроизводим случайную песню: {song}")
        else:
            QMessageBox.warning(self, "Рекомендации", "Список рекомендаций пуст")

    # --- Избранное ---
    def play_favorite(self):
        item = self.favoritesList.currentItem() # тут бд
        if item:
            song = item.text()
            QMessageBox.information(self, "Избранное", f"Воспроизводим: {song}")
        else:
            QMessageBox.warning(self, "Избранное", "Выберите песню из списка")

    # --- Загрузка песен ---
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

        if not song_name:
            QMessageBox.warning(self, "Ошибка", "Введите название песни")
            return
        if not avatar_path:
            QMessageBox.warning(self, "Ошибка", "Выберите аватар")
            return
        if not song_path:
            QMessageBox.warning(self, "Ошибка", "Выберите файл песни")
            return

        self.uploadStatus.setText(f"Песня '{song_name}' загружена!")
        QMessageBox.information(self, "Загрузка", f"Песня '{song_name}' успешно загружена")
        # Очистка полей
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
