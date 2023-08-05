from pydantic import BaseModel
from decimal import Decimal
from typing import Any
import orjson
from sqlalchemy.engine import RowMapping
def obj2dict(obj:Any)->Any:#type: ignore
    if hasattr(obj,'__tablename__') or isinstance(obj,BaseModel):
        return obj.dict()

    elif isinstance(obj,Decimal):
        return str(obj)
    elif isinstance(obj,RowMapping):
        return dict(obj)
    raise Exception("object are not jsonable")

def toBytesJson(obj:Any)->bytes:
    return orjson.dumps(obj,default=obj2dict)

def toJson(obj:Any,striplang:str='')->str:
    return orjson.dumps(obj,default=obj2dict).decode()