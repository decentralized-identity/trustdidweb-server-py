from typing import Union, List, Dict
from pydantic import BaseModel, Field
from .di_proof import DataIntegrityProof

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
    context: Union[str, List[str]] = Field(["https://www.w3.org/ns/did/v1"], alias="@context")
    id: str = Field(None)
    controller: str = Field(None)
    alsoKnownAs: List[str] = Field(None)
    verificationMethod: List[VerificationMethod] = Field(None)
    authentication: List[Union[str, VerificationMethod]] = Field(None)
    assertionMethod: List[Union[str, VerificationMethod]] = Field(None)
    keyAgreement: List[Union[str, VerificationMethod]] = Field(None)
    capabilityInvocation: List[Union[str, VerificationMethod]] = Field(None)
    capabilityDelegation: List[Union[str, VerificationMethod]] = Field(None)
    service: List[Service] = Field(None)
    proof: Union[DataIntegrityProof, List[DataIntegrityProof]] = Field(None)
