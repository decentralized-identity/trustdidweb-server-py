from typing import Dict, Any
from pydantic import BaseModel, Field, field_validator


class BaseModel(BaseModel):
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        return super().model_dump(by_alias=True, exclude_none=True, **kwargs)


class DataIntegrityProof(BaseModel):
    type: str = Field("DataIntegrityProof")
    cryptosuite: str = Field("eddsa-jcs-2022")
    verification_method: str = Field(alias="verificationMethod")
    proof_value: str = Field(alias="proofValue")
    proof_purpose: str = Field(alias="proofPurpose")
    domain: str = Field(None)
    challenge: str = Field(None)
    created: str = Field(None)
    expires: str = Field(None)

    @field_validator("type")
    @classmethod
    def validate_type(cls, value):
        assert value == "DataIntegrityProof"
        return value

    @field_validator("cryptosuite")
    @classmethod
    def validate_cryptosuite(cls, value):
        assert value in ["eddsa-jcs-2022"]
        return value

    @field_validator("expires")
    @classmethod
    def validate_expires(cls, value):
        return value
