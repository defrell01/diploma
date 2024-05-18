from http import HTTPStatus
from ..models.code_model import Code
from fastapi import APIRouter, Depends, HTTPException
from ..tools.code_runner import CodeRunner


class SandboxRouter(APIRouter):
    def __init__(
        self,
    ):
        super().__init__()

    async def run_code(self, entry: Code):
        try:
            if entry.language in ("golang", "python"):
                code_runner = CodeRunner(entry.language, entry.code)
                result = code_runner.run_container()
                return {"result": result}
            else:
                raise HTTPException(status_code=HTTPStatus.NOT_ACCEPTABLE, detail="Language not supported")
        except Exception as e:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    