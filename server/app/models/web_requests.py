from typing import Union, List, Dict
from pydantic import BaseModel, Field, AliasChoices, field_validator


class RegisterDID(BaseModel):
    didDocument: dict = Field()
