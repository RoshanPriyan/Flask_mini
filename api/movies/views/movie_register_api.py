from flask import request
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from config import session
from global_utils import success_response, error_response, CustomException
from api.movies.models import MovieList
from api.movies.utils import token_validation


def movie_register_api():
    try:
        token = request.headers.get("token")

        if not token_validation(token):
            raise CustomException(
                status_code=HTTPStatus.UNAUTHORIZED,
                details="Invalid or missing token [admin user]. Access denied.",
            )

        data = request.get_json()
        movie_name = data.get("movie_name")

        exist_name = (select(MovieList.movie_name)
                      .where(MovieList.movie_name == movie_name)
                      )
        exist_name_exc = session.execute(exist_name)
        exist_movie_name = exist_name_exc.scalars().one_or_none()

        if exist_movie_name:
            raise CustomException(
                status_code=HTTPStatus.ALREADY_REPORTED,
                details="Movie name already exists"
            )

        add_movie = MovieList(
            movie_name=data.get("movie_name"),
            release_date=data.get("release_date")
        )
        session.add(add_movie)
        session.commit()

        return success_response(
            status_code=HTTPStatus.OK,
            details="Movie register successfully"
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
            details=f"Internal server error: {e}"
        )


def movie_list_api():
    try:
        select_stmt = select(MovieList.id, MovieList.movie_name, MovieList.release_date)
        select_stmt_exe = session.execute(select_stmt)
        res = [
            {
                "id": data["id"],
                "movie_name": data["movie_name"],
                "release_date": data["release_date"].strftime("%Y-%m-%d")
            }
            for data in select_stmt_exe.mappings().all()
        ]

        return success_response(
            status_code=HTTPStatus.OK,
            details="Movie list retrieved successfully",
            data=res
        )

    except Exception as e:
        return error_response(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=e
        )