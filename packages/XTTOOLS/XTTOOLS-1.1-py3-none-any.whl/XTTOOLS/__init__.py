
from typing import Any
from starlette.responses import JSONResponse
from .xtjson import toJson,toBytesJson,obj2dict


class XTJsonResponse(JSONResponse):
    media_type = "application/json"
    def __init__(
        self,
        content: Any,
        **kwargs: Any
    ) -> None:
        super().__init__(content, **kwargs)
    def render(self, content: Any) -> bytes:
        return toBytesJson(content)
