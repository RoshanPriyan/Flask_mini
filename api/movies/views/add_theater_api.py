from flask import request
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from config import session
from global_utils import success_response, CustomException, error_response
from api.movies.models import TheaterModel,MovieList, SeatArrangementModel


def register_theater_api():
    try:
        data = request.get_json()
        movie_name = data.get("movie_name")
        theater_name = data.get("theater_name")
        total_seat = data.get("total_seat")
        row_count = data.get("row_count")
        column_count = data.get("column_count")

        movie_exist = select(MovieList.id).where(MovieList.movie_name == movie_name)
        movie_exist_exe = session.execute(movie_exist)
        movie_id = movie_exist_exe.scalar_one_or_none()

        if not movie_id:
            raise CustomException(
                status_code=HTTPStatus.NOT_FOUND,
                details="movie not found"
            )

        add_theater = TheaterModel(
            theater_name=theater_name,
            total_seat=total_seat,
            available_seat=total_seat,
            movie_name=movie_id
        )
        session.add(add_theater)
        session.flush()

        theater_id = add_theater.id

        seat_arrangement = SeatArrangementModel(
            theater_id=theater_id,
            row_count=row_count,
            column_count=column_count
        )
        session.add(seat_arrangement)
        session.commit()

        return success_response(
            status_code=HTTPStatus.OK,
            details="New theater added successfully"
        )
    except CustomException as e:
        return error_response(
            status_code=e.status_code,
            details=e.details)
    except SQLAlchemyError as e:
        session.rollback()
        return error_response(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=f"{e}"
        )
