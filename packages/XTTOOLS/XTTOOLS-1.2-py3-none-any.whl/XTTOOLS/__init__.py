
from typing import Any
from starlette.responses import JSONResponse
from .xtjson import toJson,toBytesJson,obj2dict
from starlette.responses import Response
import typing
from starlette.background import BackgroundTask
class XTJsonResponse(Response):
    media_type = "application/json"

    def __init__(
        self,
        content: typing.Any,
        status_code: int = 200,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        media_type: typing.Optional[str] = None,
        background: typing.Optional[BackgroundTask] = None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)
    def render(self, content: Any) -> bytes:
        return toBytesJson(content)
