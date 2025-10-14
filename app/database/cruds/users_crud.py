from sqlalchemy.orm import Session
from typing import Type

from app.database.models import UserSession



def create_user(db: Session, username: str, password: str) -> UserSession:
    """
    Создает нового пользователя в базе данных.
    Добавляет объект UserSession в сессию, коммитит и возвращает его.
    """
    session = UserSession(
        username=username,
        password=password
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_user_by_username(db: Session, username: str) -> Type[UserSession] | None:
    """
    Получает пользователя из базы по username.
    Возвращает объект UserSession или None, если пользователь не найден.
    """
    return db.query(UserSession).filter(UserSession.username == username).first()
