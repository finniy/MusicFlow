from sqlalchemy.orm import Session
from app.database.models import Favorite, Song

def add_to_favourites(db: Session, user_id: int, song_id: int) -> Favorite:
    """Добавить песню в избранное"""
    fav = Favorite(user_id=user_id, song_id=song_id)
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return fav


def remove_from_favourites(db: Session, user_id: int, song_id: int) -> bool:
    """Удалить песню из избранного"""
    fav = db.query(Favorite).filter_by(user_id=user_id, song_id=song_id).first()
    if fav:
        db.delete(fav)
        db.commit()
        return True
    return False


def get_user_favourites(db: Session, user_id: int) -> list:
    """Получить все избранные песни пользователя"""
    return (
        db.query(Song).join(Favorite, Favorite.song_id == Song.id)
        .filter(Favorite.user_id == user_id)
        .all()
    )
