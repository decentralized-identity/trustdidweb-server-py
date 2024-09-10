from typing import Union, List, Dict, Any
from pydantic import BaseModel, Field
from .did_document import DidDocument
from config import settings

class BaseRequest(BaseModel):
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        return super().model_dump(by_alias=True, exclude_none=True, **kwargs)


class RequestDID(BaseRequest):
    namespace: str = Field(example="example")
    identifier: str = Field(example="issuer")


class RegisterDID(BaseRequest):
    didDocument: DidDocument = Field(example={
        "@context": [],
        "id": f"{settings.DID_WEB_BASE}:example:issuer"
    })


class RequestDIDUpgrade(BaseRequest):
    id: str = Field(example=f"{settings.DID_WEB_BASE}:example:issuer")
    updateKey: str = Field(example="z...")
    

class PublishLogEntry(BaseRequest):
    logEntry: list = Field()
