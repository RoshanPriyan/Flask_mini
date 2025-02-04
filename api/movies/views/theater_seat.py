from flask import request
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from config import session
from global_utils import success_response, CustomException, error_response
from api.movies.models import TheaterModel, SeatArrangementModel

def theater_seat_api():
    try:
        theater_name = request.get_json()
        stmt = (
            select(
                TheaterModel.theater_name,
                SeatArrangementModel.theater_id,
                SeatArrangementModel.row_count,
                SeatArrangementModel.column_count
            ).select_from(TheaterModel).join(SeatArrangementModel, TheaterModel.id == SeatArrangementModel.theater_id)
                .where(TheaterModel.theater_name == theater_name.get("theater_name"))
        )
        stmt_exe = session.execute(stmt)
        theater_data = stmt_exe.mappings().first()

        if not theater_data:
            raise CustomException(
                status_code=HTTPStatus.NOT_FOUND,
                details="Theater name not found"
            )

        data = dict(theater_data)
        custom_dict = {}
        for i in data.get("row_count"):
            row = []
            key = f"ROW: {i}"
            for j in range(1, data.get("column_count") + 1):
                row_column = i + str(j)
                row.append(row_column)
            custom_dict[key] = row
        data["theater_row"] = custom_dict

        return success_response(
            status_code=HTTPStatus.OK,
            details="Theater seats retrieved successfully",
            data=data
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