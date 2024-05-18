from datetime import timedelta
from http import HTTPStatus
from fastapi import APIRouter, Depends

from app.auth.auth import AuthUtils
from app.database.db import create_student, create_user, offer_student
from app.models.request_models import RegUser, User


class ParentRouter(APIRouter):
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

            if creation_res == 1:
                return {"login": entry.email, "password": entry.password, "status": 1}
            else:
                return HTTPStatus.NOT_ACCEPTABLE

        except Exception as e:
            print(e)
            return HTTPStatus.INTERNAL_SERVER_ERROR

    async def reg_student(
        self,
        entry: RegUser,
        current_user: RegUser = Depends(AuthUtils().get_current_user),
    ):
        if current_user.role == "parent":
            try:
                entry.password = self.auth_instance.get_password_hash(entry.password)

                creation_res = await create_student(entry, current_user.email)

                if creation_res:
                    return {
                        "message": "child created",
                        "email": entry.email,
                        "password": entry.password,
                    }
                return HTTPStatus.INTERNAL_SERVER_ERROR
            except Exception as e:
                print(e)
                return HTTPStatus.INTERNAL_SERVER_ERROR
            
    async def choose_tutor(
            self,
            entry: RegUser,
            current_user: RegUser = Depends(AuthUtils().get_current_user)
    ):
        if current_user.role == "parent" or current_user.role == "child":
            result = await offer_student(current_user, entry.email)

            if result == 1:
                return {"message": "offer sent"}
            elif result == -1:
                return { "message": "tutor not found"}
            else:
                return { "message": "child not found"}

        else:
            return HTTPStatus.UNAUTHORIZED

