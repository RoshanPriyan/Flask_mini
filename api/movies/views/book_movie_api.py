from flask import request
from http import HTTPStatus
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from config import session
from global_utils import success_response, CustomException, error_response
from api.movies.models import BookMovieModel, MovieList, TheaterModel


def book_movie_api():
    try:
        data = request.get_json()
        movie_name = data.get("movie_name")
        theater_name = data.get("theater_name")
        booking_seat = data.get("seat")

        movie_exist = (
            select(
                MovieList.id.label("movie_id"),TheaterModel.id.label("theater_id"),TheaterModel.available_seat,
                TheaterModel.booked_seat, TheaterModel.total_seat
            )
            .select_from(MovieList)
            .join(TheaterModel, MovieList.id == TheaterModel.movie_name)
            .where(MovieList.movie_name == movie_name, TheaterModel.theater_name == theater_name)
                       )
        movie_exist_exe = session.execute(movie_exist)
        movie_data = movie_exist_exe.mappings().first()

        if not movie_data:
            raise CustomException(
                status_code=HTTPStatus.NOT_FOUND,
                details="Movie name not found"
            )

        movie_id = movie_data.get("movie_id")
        theater_id = movie_data.get("theater_id")
        already_available_seat = movie_data.get("available_seat")
        already_booked_seat = movie_data.get("booked_seat")

        if not booking_seat <= already_available_seat:
            raise CustomException(
                status_code=HTTPStatus.BAD_REQUEST,
                details="Seats not available" if already_available_seat == 0 else f"Seats not available, only {already_available_seat} available"
            )

        book_movie = BookMovieModel(
            theater_id=theater_id,
            movie_id=movie_id,
            seat_book=booking_seat
        )
        session.add(book_movie)
        session.flush()

        current_booked_seat = book_movie.seat_book
        total_booked_seat = current_booked_seat + already_booked_seat
        total_available_seat = already_available_seat - booking_seat

        update_seat = (
            update(TheaterModel)
            .where((TheaterModel.theater_name == theater_name) & (TheaterModel.movie_name == movie_id))
            .values(booked_seat=total_booked_seat, available_seat=total_available_seat)
        )
        session.execute(update_seat)
        session.commit()

        return success_response(
            status_code=HTTPStatus.OK,
            details="Booking successfully"
        )

    except CustomException as e:
        return error_response(
            status_code=e.status_code,
            details=e.details
        )
    except SQLAlchemyError as e:
        session.rollback()
        return error_response(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=e
        )
