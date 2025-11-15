import os
import random
from PyQt6 import uic
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QListWidgetItem, QFileDialog
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from app.database.session import session_local
from app.database.cruds.song_crud import get_all_songs, create_song
from app.database.cruds.favourite_crud import (
    get_user_favourites,
    add_to_favourites,
    remove_from_favourites,
    is_in_favourites,
)
from app.utils.file_storage import save_uploaded_file


class MainWindow(QMainWindow):
    def __init__(self, current_user_id: int):
        super().__init__()
        self.current_user_id = current_user_id
        self.initUI()

    def initUI(self) -> None:
        """Инициализация главного окна и плеера."""
        # Плейлист и текущий трек
        self.current_playlist = []
        self.current_index = -1

        # Пути для хранения медиафайлов
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.media_songs_dir = os.path.join(self.base_dir, "media", "songs")
        self.media_covers_dir = os.path.join(self.base_dir, "media", "covers")
        os.makedirs(self.media_songs_dir, exist_ok=True)
        os.makedirs(self.media_covers_dir, exist_ok=True)

        # Плеер
        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)

        self.load_ui()
        self.wire_events()
        self.load_library()
        self.refresh_favorites()

    def load_ui(self) -> None:
        """Загрузка интерфейса и установка начальных параметров."""
        self.setWindowTitle("MusicFlow — Плеер")

        # Поиск UI файла
        ui_paths = [
            "ui/main_window.ui",
            "../ui/main_window.ui"
        ]

        for ui_path in ui_paths:
            if os.path.exists(ui_path):
                uic.loadUi(ui_path, self)
                break
        else:
            ui_path = os.path.join(self.base_dir, "ui", "main_window.ui")
            uic.loadUi(ui_path, self)

        self.volumeSlider.setValue(50)
        self.audio_output.setVolume(0.5)

    def wire_events(self) -> None:
        """Подключение сигналов к слотам."""
        self.playPauseButton.clicked.connect(self.toggle_play_pause)
        self.nextTrackButton.clicked.connect(self.play_next)
        self.prevTrackButton.clicked.connect(self.play_prev)
        self.favoriteButton.clicked.connect(self.toggle_favorite_current)
        self.volumeSlider.valueChanged.connect(self.volume_changed)

        self.recommendationList.itemDoubleClicked.connect(self.play_selected_recommendation)
        self.favoritesList.itemDoubleClicked.connect(self.play_selected_favorite)

        self.chooseAvatarButton.clicked.connect(self.choose_cover)
        self.chooseFileButton.clicked.connect(self.choose_song)
        self.uploadButton.clicked.connect(self.upload_song)

        self.player.playbackStateChanged.connect(self.update_play_button_icon)

    def load_library(self) -> None:
        """Загрузка всех песен из базы данных."""
        with session_local() as db:
            self.current_playlist = get_all_songs(db)
        self.recommendationList.clear()
        for song in self.current_playlist:
            self.recommendationList.addItem(QListWidgetItem(song.title))

    def refresh_favorites(self) -> None:
        """Обновление списка избранных песен."""
        with session_local() as db:
            favorites = get_user_favourites(db, self.current_user_id)
        self.favoritesList.clear()
        for song in favorites:
            item = QListWidgetItem(song.title)
            item.setData(Qt.ItemDataRole.UserRole, song.id)
            self.favoritesList.addItem(item)

    def display_song(self, song) -> None:
        """Отображение информации о текущем треке и его обложки."""
        self.trackTitleLabel.setText(song.title or "—")

        try:
            pix = QPixmap(song.cover_path) if song.cover_path else QPixmap()
            if not pix.isNull():
                self.trackCoverLabel.setPixmap(
                    pix.scaled(320, 320, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                )
            else:
                self.trackCoverLabel.setPixmap(QPixmap())
        except Exception:
            self.trackCoverLabel.setPixmap(QPixmap())

        try:
            with session_local() as db:
                fav = is_in_favourites(db, self.current_user_id, song.id)
            self.favoriteButton.setText("❤️" if fav else "♡")
        except Exception:
            self.favoriteButton.setText("♡")

    def play_song(self, index: int) -> None:
        """Воспроизведение трека по индексу."""
        if not self.current_playlist:
            return
        if index < 0 or index >= len(self.current_playlist):
            return

        self.current_index = index
        song = self.current_playlist[index]

        url = QUrl.fromLocalFile(os.path.abspath(song.file_path))
        self.player.setSource(url)
        self.player.play()
        self.display_song(song)

    def toggle_play_pause(self) -> None:
        """Переключение между воспроизведением и паузой."""
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            if self.current_index == -1 and self.current_playlist:
                random_index = random.randint(0, len(self.current_playlist) - 1)
                self.play_song(random_index)
            else:
                self.player.play()

    def update_play_button_icon(self) -> None:
        """Обновление иконки кнопки воспроизведения."""
        state = self.player.playbackState()
        self.playPauseButton.setText("⏸" if state == QMediaPlayer.PlaybackState.PlayingState else "▶️")

    def play_next(self) -> None:
        """Воспроизведение случайного следующего трека."""
        if not self.current_playlist:
            return
        random_index = random.randint(0, len(self.current_playlist) - 1)
        self.play_song(random_index)

    def play_prev(self) -> None:
        """Воспроизведение случайного предыдущего трека."""
        if not self.current_playlist:
            return
        random_index = random.randint(0, len(self.current_playlist) - 1)
        self.play_song(random_index)

    def toggle_favorite_current(self) -> None:
        """Добавление или удаление текущего трека из избранного."""
        if not (0 <= self.current_index < len(self.current_playlist)):
            return
        song = self.current_playlist[self.current_index]

        with session_local() as db:
            if is_in_favourites(db, self.current_user_id, song.id):
                remove_from_favourites(db, self.current_user_id, song.id)
                self.favoriteButton.setText("♡")
            else:
                add_to_favourites(db, self.current_user_id, song.id)
                self.favoriteButton.setText("❤️")
        self.refresh_favorites()

    def volume_changed(self, value: int) -> None:
        """Изменение громкости плеера."""
        self.audio_output.setVolume(max(0.0, min(1.0, value / 100.0)))

    def play_selected_recommendation(self, item: QListWidgetItem) -> None:
        """Воспроизведение трека из списка рекомендаций по двойному клику."""
        title = item.text()
        for idx, song in enumerate(self.current_playlist):
            if song.title == title:
                self.play_song(idx)
                break

    def play_selected_favorite(self, item: QListWidgetItem) -> None:
        """Воспроизведение трека из списка избранного по двойному клику."""
        song_id = item.data(Qt.ItemDataRole.UserRole)
        if song_id is None:
            return
        for idx, song in enumerate(self.current_playlist):
            if song.id == song_id:
                self.play_song(idx)
                break

    def choose_cover(self):
        """Выбор обложки для загружаемой песни."""
        path, _ = QFileDialog.getOpenFileName(self, "Выберите обложку", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.avatarPathLabel.setText(path)
            pix = QPixmap(path)
            if not pix.isNull():
                self.uploadCoverPreview.setPixmap(
                    pix.scaled(240, 240, Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
                )

    def choose_song(self):
        """Выбор аудиофайла для загрузки."""
        path, _ = QFileDialog.getOpenFileName(self, "Выберите песню", "", "Audio Files (*.mp3 *.wav *.ogg)")
        if path:
            self.filePathLabel.setText(path)

    def upload_song(self):
        """Загрузка новой песни в базу и локальное хранилище."""
        title = self.songNameInput.text().strip()
        src_song = self.filePathLabel.text().strip()
        src_cover = self.avatarPathLabel.text().strip()

        if not title or not src_song or not src_cover:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        song_path = save_uploaded_file(src_song, self.media_songs_dir)
        cover_path = save_uploaded_file(src_cover, self.media_covers_dir)

        with session_local() as db:
            create_song(db, title=title, file_path=song_path, cover_path=cover_path, artist_id=self.current_user_id)

        self.load_library()
        self.refresh_favorites()

        QMessageBox.information(self, "Загрузка", f"Песня '{title}' успешно загружена")
        self.songNameInput.clear()
        self.avatarPathLabel.clear()
        self.filePathLabel.clear()
        self.uploadCoverPreview.setPixmap(QPixmap())
