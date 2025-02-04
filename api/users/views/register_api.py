from flask import request
from sqlalchemy import select
from http import HTTPStatus
from sqlalchemy.exc import SQLAlchemyError
from config import session
from global_utils import success_response, CustomException, error_response
from api.users.utils import state_id_fun, generate_token
from api.users.models import UserModel, UserAuthInfoModel

def register_api():
    try:
        data = request.get_json()
        username = data.get("username")
        state_id = state_id_fun(data.get("state_name"))

        existing_user = select(UserModel.username).where(UserModel.username==username)
        res_exist_user = session.execute(existing_user)
        exist_user = res_exist_user.scalars().first()

        if exist_user:
            raise CustomException(
                status_code=HTTPStatus.BAD_REQUEST,
                details="username already exist"
            )

        add_data = UserModel(
            username= username,
            email= data.get("email"),
            city=data.get("city"),
            state_id=state_id,
            hash_password=data.get("password"),
            role=data.get("role")
        )

        session.add(add_data)
        session.flush()
        user_id = add_data.id
        add_auth_info = UserAuthInfoModel(
            token=generate_token(user_id),
            user_id=user_id
        )
        session.add(add_auth_info)
        session.commit()

        return success_response(
            details="user register successfully"
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
