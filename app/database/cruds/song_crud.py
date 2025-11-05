from typing import Optional, List
from sqlalchemy.orm import Session

from app.database.models import Song


def create_song(
        db: Session,
        title: str,
        file_path: str,
        cover_path: str,
        artist_id: Optional[int] = None,
) -> Song:
    """Создание новой песни."""
    song = Song(
        title=title,
        file_path=file_path,
        cover_path=cover_path,
        artist_id=artist_id,
    )
    db.add(song)
    db.commit()
    db.refresh(song)
    return song


def get_song_by_id(db: Session, song_id: int) -> Optional[Song]:
    """Получить песню по ID"""
    return db.query(Song).filter(Song.id == song_id).first()


def get_all_songs(db: Session) -> List[Song]:
    """Получить все песни"""
    return db.query(Song).all()


def delete_song(db: Session, song_id: int) -> bool:
    """Удалить песню"""
    song = db.query(Song).filter(Song.id == song_id).first()
    if song:
        db.delete(song)
        db.commit()
        return True
    return False
