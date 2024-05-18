import os
from fastapi import FastAPI

from app.endpoints.sandbox import SandboxRouter

async def create_app():
    app = FastAPI()

    sandbox_router_instance = SandboxRouter()

    sandbox_router_instance.add_api_route(
        "/api/run_code/", sandbox_router_instance.run_code, methods=["POST"]
    )

    app.include_router(sandbox_router_instance)

    return app
