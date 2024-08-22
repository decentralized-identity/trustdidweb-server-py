from typing import Union, List, Dict
from pydantic import BaseModel, Field, AliasChoices, field_validator


class StatusListCredential(BaseModel):
    context: List[str] = Field(alias="@context")
    type: List[str] = Field()
    id: str = Field()
    issuer: str = Field()
    credential_subject: dict = Field(alias="credentialSubject")
    proof: dict = Field()


class DidCredential(BaseModel):
    id: str = Field(None)
    type: List[str] = Field()
    context: List[str] = Field(alias="@context")
    issuance_date: str = Field(alias="issuanceDate")
    expiration_date: str = Field(None, alias="expirationDate")
    credential_subject: dict = Field(alias="credentialSubject")
