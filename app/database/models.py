from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database.session import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    song_id = Column(Integer, ForeignKey("songs.id", ondelete="CASCADE"))
    added_date = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="favorites")
    song = relationship("Song", back_populates="favorited_by")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    favorites = relationship("Favorite", back_populates="user")


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    file_path = Column(String)
    cover_path = Column(String)
    artist_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    favorited_by = relationship("Favorite", back_populates="song")
