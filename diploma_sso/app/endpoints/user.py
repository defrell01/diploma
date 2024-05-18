from datetime import timedelta
from http import HTTPStatus
from fastapi import APIRouter, Depends

from app.auth.auth import AuthUtils
from app.database.db import create_user
from app.models.request_models import RegUser, User


class UserRouter(APIRouter):
    def __init__(
        self,
        auth_instance: AuthUtils,
    ):
        super().__init__()
        self.auth_instance: AuthUtils = auth_instance

    async def reg_parent(self, entry: RegUser):
        try:
            entry.password = self.auth_instance.get_password_hash(entry.password)

            creation_res = await create_user(entry)

            if creation_res:
                return {"login": entry.email, "password": entry.password, "status": 1}
            else:
                return HTTPStatus.NOT_ACCEPTABLE

        except Exception as e:
            print(e)
            return HTTPStatus.INTERNAL_SERVER_ERROR

    async def create_tutor(
        self, entry: RegUser, current_user: dict = Depends(AuthUtils().get_current_user)
    ):
        try:
            if not current_user:
                return HTTPStatus.UNAUTHORIZED

            if current_user.role != "admin":
                return HTTPStatus.UNAUTHORIZED

            password_lng = 6
            tmp_password = self.auth_instance.generate_password(password_lng)
            entry.password = self.auth_instance.get_password_hash(tmp_password)

            creation_res = await create_user(entry)

            if creation_res:
                return {
                    "login": entry.login,
                    "password:": tmp_password,
                    "status": 1,
                }

            return HTTPStatus.CONFLICT
        except Exception as e:
            print(e)
            return HTTPStatus(400)

    async def token(self, entry: User):
        try:
            print("trying auth_user")
            user = await self.auth_instance.auth_user(entry)
            if user:
                access_token_expires = timedelta(
                    minutes=self.auth_instance.ACCESS_TOKEN_EXPIRE_MINUTES
                )
                access_token = self.auth_instance.create_access_token(
                    data={"sub": user.email}, expires_delta=access_token_expires
                )
                return {"access_token": access_token, "token_type": "bearer"}
            return HTTPStatus(401)
        except Exception as e:
            print(e)
            return HTTPStatus(400)
