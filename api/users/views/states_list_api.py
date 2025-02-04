from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from config import session
from global_utils import success_response, error_response
from api.users.models import StatesModel


def states_list_api():
    try:
        list_state = select(StatesModel.state_name)
        list_state_res = session.execute(list_state)
        states = dict(list_state_res.mappings().first())

        return success_response(
            status_code=HTTPStatus.OK,
            details="states details retrieve successfully",
            data=states
        )

    except SQLAlchemyError as e:
        return error_response(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            details=f"Internal server error: {str(e)}"
        )