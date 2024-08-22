from typing import Union, List, Dict
from pydantic import BaseModel, Field, AliasChoices, field_validator


class DataIntegrityProof(BaseModel):
    type: str = Field("DataIntegrityProof")
    cryptosuite: str = Field("eddsa-jcs-2022")
    verification_method: str = Field(alias="verificationMethod")
    proof_value: str = Field(alias="proofValue")
    proof_purpose: str = Field(alias="proofPurpose")

    @field_validator("type")
    @classmethod
    def validate_type(cls, value):
        if value != "DataIntegrityProof":
            raise ValueError("Expected 'DataIntegrityProof' type")
        return value

    @field_validator("cryptosuite")
    @classmethod
    def validate_cryptosuite(cls, value):
        if value not in ["eddsa-jcs-2022"]:
            raise ValueError("Unsupported cryptosuite")
        return value
