from datetime import timedelta
from http import HTTPStatus
from fastapi import APIRouter, Depends

from app.auth.auth import AuthUtils
from app.database.db import create_student, create_user, get_all_users
from app.models.request_models import RegUser, User


class CommonRouter(APIRouter):
    def __init__(
        self,
        auth_instance: AuthUtils,
    ):
        super().__init__()
        self.auth_instance: AuthUtils = auth_instance

    async def get_users(current_user: RegUser = Depends(AuthUtils().get_current_user)):
        if not current_user:
            return HTTPStatus.UNAUTHORIZED
        else:
            users = await get_all_users()

            if len(users) > 0:
                return users
            else:
                return HTTPStatus.INTERNAL_SERVER_ERROR
