from http import HTTPStatus
import os
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.database.db import get_user
from ..models.request_models import User
from fastapi import Depends


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token/")


class AuthUtils:
    def __init__(self):
        self.context = self.create_context()
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def create_context(self) -> CryptContext:
        return CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        return self.context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.context.hash(password)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def auth_user(self, user: User):
        db_user = await get_user(user.email)

        if db_user:
            if self.verify_password(user.password, db_user.password):
                return db_user
            return None
        return None

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPStatus(401)
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return credentials_exception
            user = await get_user(username)
            if user is None:
                return credentials_exception
            return user
        except JWTError:
            return credentials_exception
