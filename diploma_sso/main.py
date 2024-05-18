import asyncio
import os

from fastapi import FastAPI
from uvicorn import Config, Server
from gunicorn.app.base import BaseApplication

from app.app import create_app


async def run_asgi(app: FastAPI):
    uvicorn_config = Config(app=app, host="0.0.0.0", port=8000)
    uvicorn_server = Server(uvicorn_config)
    await uvicorn_server.serve()


class ASGIServer(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key, value)

    def load(self):
        return self.application


async def run_with_gunicorn(app: FastAPI):
    options = {
        "bind": "0.0.0.0:8000",
        "workers": os.cpu_count() * 2 + 1,
        "worker_class": "uvicorn.workers.UvicornWorker"
    }
    server = ASGIServer(app, options=options)
    server.run()


async def main():
    use_gunicorn = int(os.getenv("USE_WSGI", 0))
    print(f'use gunicorn: {use_gunicorn}')
    app = await create_app()

    if use_gunicorn == 1:
        await run_with_gunicorn(app)
    else:
        await run_asgi(app)


if __name__ == "__main__":
    asyncio.run(main())
