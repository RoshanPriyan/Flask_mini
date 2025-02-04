from flask import request
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from config import session
from global_utils import success_response, error_response
from api.movies.models import MovieList, TheaterModel

def available_ticket_api():
    try:
        available_seat_stmt = (
            select(MovieList.movie_name, TheaterModel.theater_name, TheaterModel.total_seat, TheaterModel.booked_seat,
            TheaterModel.available_seat
                   )
            .select_from(MovieList)
            .join(TheaterModel, MovieList.id == TheaterModel.movie_name)
        )

        available_seat_exe = session.execute(available_seat_stmt)
        available_seat_data = [dict(data) for data in available_seat_exe.mappings().all()]

        return success_response(
            status_code=HTTPStatus.OK,
            details="Available ticket retrieved successfully",
            data=available_seat_data
        )

    except SQLAlchemyError as e:
        return error_response(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=e
        )
