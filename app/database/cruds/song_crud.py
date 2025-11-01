from sqlalchemy.orm import Session

from app.database.models import Song


def create_song(db: Session, song_name: str, song_path: str, avatar_path: str) -> Song:
    """Создание новой песни"""
    session = Song(
        title=song_name,
        file_path=song_path,
        cover_path=avatar_path,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_song_by_id(db: Session, song_id: int) -> Song | None:
    """Получить песню по ID"""
    return db.query(Song).filter(Song.id == song_id).first()


def get_all_songs(db: Session) -> list[Song]:
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
