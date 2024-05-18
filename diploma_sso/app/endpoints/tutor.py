from datetime import timedelta
from http import HTTPStatus
from fastapi import APIRouter, Depends

from app.auth.auth import AuthUtils
from app.database.db import create_student, create_user
from app.models.request_models import RegUser, User


class Tutor(APIRouter):
    def __init__(
        self,
        auth_instance: AuthUtils,
    ):
        super().__init__()
        self.auth_instance: AuthUtils = auth_instance

    
