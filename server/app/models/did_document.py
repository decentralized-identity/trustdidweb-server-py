from typing import Union, List, Dict, Any
from pydantic import BaseModel, Field, field_validator
from .di_proof import DataIntegrityProof
import re


class BaseModel(BaseModel):
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        return super().model_dump(by_alias=True, exclude_none=True, **kwargs)


class VerificationMethod(BaseModel):
    id: str = Field()
    type: Union[str, List[str]] = Field()
    controller: str = Field()
    publicKeyMultibase: str = Field()


class Service(BaseModel):
    id: str = Field()
    type: Union[str, List[str]] = Field()
    serviceEndpoint: str = Field()


class DidDocument(BaseModel):
    context: Union[str, List[str]] = Field(
        ["https://www.w3.org/ns/did/v1"], alias="@context"
    )
    id: str = Field()
    controller: str = Field(None)
    alsoKnownAs: List[str] = Field(None)
    verificationMethod: List[VerificationMethod] = Field()
    authentication: List[Union[str, VerificationMethod]] = Field()
    assertionMethod: List[Union[str, VerificationMethod]] = Field()
    keyAgreement: List[Union[str, VerificationMethod]] = Field(None)
    capabilityInvocation: List[Union[str, VerificationMethod]] = Field(None)
    capabilityDelegation: List[Union[str, VerificationMethod]] = Field(None)
    service: List[Service] = Field(None)

    @field_validator("context")
    @classmethod
    def validate_context(cls, value):
        assert value[0] == "https://www.w3.org/ns/did/v1", "Invalid context."
        return value

    @field_validator("id")
    @classmethod
    def validate_id(cls, value):
        DID_REGEX = re.compile(
            "did:([a-z0-9]+):((?:[a-zA-Z0-9._%-]*:)*[a-zA-Z0-9._%-]+)"
        )
        assert DID_REGEX.match(value), "Expected id to be a DID."
        return value

    @field_validator("authentication")
    @classmethod
    def validate_authentication(cls, value):
        assert len(value) >= 1, "Expected at least one authentication method."
        return value

    @field_validator("assertionMethod")
    @classmethod
    def validate_assertion_method(cls, value):
        assert len(value) >= 1, "Expected at least one assertion method."
        return value

    @field_validator("verificationMethod")
    @classmethod
    def validate_verification_method(cls, value):
        assert len(value) >= 1, "Expected at least one verification method."
        return value


class SecuredDidDocument(DidDocument):
    proof: List[DataIntegrityProof] = Field(None)

    @field_validator("proof")
    @classmethod
    def validate_proof(cls, value):
        assert len(value) == 2, "Expected proof set."
        return value
