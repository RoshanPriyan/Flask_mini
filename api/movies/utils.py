from sqlalchemy import select, and_
from api.users.models import UserAuthInfoModel, UserModel
from config import session


def token_validation(token):
    if not token:
        return False

    admin_user_stmt = (
        select(UserModel.role)
        .select_from(UserModel)
        .join(UserAuthInfoModel, UserModel.id == UserAuthInfoModel.user_id)
        .where(
            and_(
                UserAuthInfoModel.token == token,
                UserModel.role == "Admin"
            )
        )
    )
    admin_user_exe = session.execute(admin_user_stmt).mappings().first()

    return admin_user_exe is not None
