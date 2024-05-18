import os
from fastapi import FastAPI

from app.auth.auth import AuthUtils
from app.database.db import initialize_db
from app.endpoints.common import CommonRouter
from app.endpoints.parent import ParentRouter
from app.endpoints.user import UserRouter


async def create_app():
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    app = FastAPI()

    auth_util_instance = AuthUtils()

    admin_password_hash = auth_util_instance.get_password_hash(admin_password)

    print(f"admin password hash: {admin_password_hash}")

    user_router_instance = UserRouter(auth_util_instance)

    user_router_instance.add_api_route(
        "/api/token/", user_router_instance.token, methods=["POST"]
    )

    parent_router_instance = ParentRouter(auth_util_instance)

    parent_router_instance.add_api_route(
        "/api/register/", parent_router_instance.reg_parent, methods=["POST"]
    )

    parent_router_instance.add_api_route(
        "/api/register_child/", parent_router_instance.reg_student, methods=["POST"]
    )

    common_router_instance = CommonRouter(auth_util_instance)

    common_router_instance.add_api_route(
        "/api/get_all_users/", common_router_instance.get_users, methods=["POST"]
    )

    await initialize_db(admin_username, admin_password_hash)

    app.include_router(user_router_instance)
    app.include_router(parent_router_instance)
    app.include_router(common_router_instance)

    return app
