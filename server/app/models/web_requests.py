from typing import Union, List, Dict
from pydantic import BaseModel, Field
from .did_document import DidDocument

class RegisterDID(BaseModel):
    didDocument: DidDocument = Field()
