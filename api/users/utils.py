from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
import os
import binascii
import time
from .models import StatesModel, UserAuthInfoModel
from config import session
from global_utils import CustomException


def state_id_fun(state_name):
    try:
        print(state_name)
        select_stmt = select(StatesModel.id).where(StatesModel.state_name.like(f"%{state_name}%"))
        exe_stmt = session.execute(select_stmt)
        state_id = exe_stmt.scalars().first()

        if state_id is None:
            raise CustomException(
                status_code=HTTPStatus.NOT_FOUND,
                details="Please provide a valid state name"
            )

        return state_id

    except SQLAlchemyError as e:
        raise CustomException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=f"Internal server error: {str(e)}"
        )


def time_int():
    return int(time.time())


def generate_token(user_id):
    random_bytes = os.urandom(16)
    random_hex = binascii.hexlify(random_bytes).decode()
    timestamp = time_int()
    token = f"{random_hex}{user_id}{timestamp}"
    return token


def validate_token(token):
    if not token:
        return False
    try:
        validate_token_stmt = select(UserAuthInfoModel).where(UserAuthInfoModel.token == token)
        result = session.execute(validate_token_stmt).scalar_one_or_none()
        return result is not None
    except Exception as e:
        return False
