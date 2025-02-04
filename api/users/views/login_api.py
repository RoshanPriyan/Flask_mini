from flask import request
from sqlalchemy import select, update
from http import HTTPStatus
import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from config import session
from global_utils import success_response, CustomException, error_response
from api.users.models import UserModel, StatesModel, UserAuthInfoModel
from api.users.utils import generate_token


def login_api():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        find_user = select(UserModel.username, UserModel.hash_password).where(UserModel.username == username)
        res_find_user = session.execute(find_user)
        final_user = res_find_user.mappings().first()

        if final_user:
            user_id_stmt = select(UserModel.id).where(UserModel.username == final_user.get("username"))
            user_id_res = session.execute(user_id_stmt)
            user = user_id_res.mappings().first()

            user_id = user.get("id")

            refresh_token = update(UserAuthInfoModel).where(UserAuthInfoModel.user_id == user_id).values(
                token=generate_token(user_id)
            )
            session.execute(refresh_token)
            session.commit()

        if not final_user:
            raise CustomException(
                status_code=HTTPStatus.NOT_FOUND.value,
                details="User not found"
            )

        is_valid = bcrypt.checkpw(password.encode('utf-8'), final_user["hash_password"].encode('utf-8'))

        if not is_valid:
            raise CustomException(
                status_code=HTTPStatus.UNAUTHORIZED.value,
                details="Invalid password"
            )
        if is_valid:
            user_data_query = (
                select(
                    UserModel.id,
                    UserModel.username,
                    UserModel.city,
                    StatesModel.state_code,
                    StatesModel.state_name,
                    UserModel.email,
                    UserModel.created_date,
                    UserAuthInfoModel.token
                )
                .select_from(UserModel)
                .join(StatesModel, UserModel.state_id == StatesModel.id)
                .join(UserAuthInfoModel, UserModel.id == UserAuthInfoModel.user_id)
                .where(UserModel.username == username)
            )
            user_data_res = session.execute(user_data_query)
            user_data = dict(user_data_res.mappings().first())

            created_date = user_data["created_date"]
            user_data["created_date"] = created_date.strftime("%Y-%m-%d %H:%M:%S")

            city = user_data.pop("city")
            state = user_data.pop("state_name")
            user_data["location"] = f"{city}, {state}"

        return success_response(
            details="User login successfully",
            data=user_data
        )

    except CustomException as e:
        return error_response(
            status_code=e.status_code,
            details=e.details
        )
    except SQLAlchemyError as e:
        return error_response(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            details=f"Internal server error: {str(e)}"
        )
