from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, JSON
from datetime import datetime, date
from sqlalchemy.orm import relationship
from config import Base


class MovieList(Base):
    __tablename__ = "movie_list"

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_name = Column(String(50), nullable=False, unique=True)
    release_date = Column(Date, nullable=False, default=date.today)
    update_date = Column(DateTime, nullable=False, default=datetime.now)

    theater = relationship("TheaterModel", back_populates="movie")
    b_movie = relationship("BookMovieModel", back_populates="movie")
    seat = relationship("SeatsModel", back_populates="mid")


class TheaterModel(Base):
    __tablename__ = "theaters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    theater_name = Column(String(50), nullable=False)
    total_seat = Column(String(50), nullable=False)
    available_seat = Column(String(50), nullable=True, default=0)
    booked_seat = Column(String(50), nullable=True, default=0)
    movie_name = Column(Integer, ForeignKey("movie_list.id"), nullable=False)

    movie = relationship("MovieList", back_populates="theater")
    b_movie = relationship("BookMovieModel", back_populates="theater")
    seat = relationship("SeatsModel", back_populates="tid")

class BookMovieModel(Base):
    __tablename__ = "book_movie"

    id = Column(Integer, primary_key=True, autoincrement=True)
    theater_id = Column(Integer, ForeignKey("theaters.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movie_list.id"), nullable=False)
    seat_book = Column(Integer, nullable=True)

    theater = relationship("TheaterModel", back_populates="b_movie")
    movie = relationship("MovieList", back_populates="b_movie")


class SeatsModel(Base):
    __tablename__ = "seats"

    seat_id = Column(Integer, primary_key=True, autoincrement=True)
    seat_row = Column(String)
    seat_column = Column(Integer)
    theater_id = Column(Integer, ForeignKey("theaters.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movie_list.id"), nullable=False)

    mid = relationship("MovieList", back_populates="seat")
    tid = relationship("TheaterModel", back_populates="seat")


class SeatArrangementModel(Base):
    __tablename__ = "seat_arrangement"

    id = Column(Integer, primary_key=True, autoincrement=True)
    theater_id = Column(Integer, ForeignKey("theaters.id"))
    row_count = Column(JSON)
    column_count = Column(Integer)
