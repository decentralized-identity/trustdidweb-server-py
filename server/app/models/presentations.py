from typing import Union, List, Dict
from pydantic import BaseModel, Field, AliasChoices, field_validator


class VerifiablePresentation(BaseModel):
    context: List[str] = Field("https://www.w3.org/ns/credentials/v2", alias="@context")
    type: List[str] = Field("VerifiablePresentation")
    holder: str = Field()
    credential_subject: List[dict] = Field(alias="credentialSubject")
    proof: dict = Field()

    @field_validator("context")
    @classmethod
    def validate_context(cls, value):
        if value[0] != "https://www.w3.org/ns/credentials/v2":
            raise ValueError("Expected 'https://www.w3.org/ns/credentials/v2' context")
        return value

    @field_validator("type")
    @classmethod
    def validate_type(cls, value):
        if value != "VerifiablePresentation":
            raise ValueError("Expected 'VerifiablePresentation' type")
        return value

    @field_validator("proof")
    @classmethod
    def validate_proof(cls, value):
        if value["proofPurpose"] != "authentication":
            raise ValueError("Expected 'authentication' proofPurpose")
        return value
