from flask import request
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from config import session
from global_utils import success_response, CustomException, error_response
from api.movies.models import TheaterModel, SeatArrangementModel, MovieList


def book_seat_api():
    try:
        data = request.get_json()
        movie_name = data.get("movie_name")
        theater_name = data.get("theater_name")

        movie_exist = (
            select(
                MovieList.id.label("movie_id"), TheaterModel.id.label("theater_id"), TheaterModel.available_seat,
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

        return success_response(
            status_code=HTTPStatus.OK,
            details="Theater seats retrieved successfully",
            data="data"
        )
    except CustomException as e:
        return error_response(
            status_code=e.status_code,
            details=e.details
        )
    except SQLAlchemyError as e:
        return error_response(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            details=e
        )