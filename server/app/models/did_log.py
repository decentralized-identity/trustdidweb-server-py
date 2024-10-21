from typing import Union, List, Dict, Any
from pydantic import BaseModel, Field
from .did_document import DidDocument
from .di_proof import DataIntegrityProof


class BaseModel(BaseModel):
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        return super().model_dump(by_alias=True, exclude_none=True, **kwargs)


class Witness(BaseModel):
    id: str = Field(None)
    weight: int = Field(None)


class WitnessParam(BaseModel):
    threshold: int = Field(None)
    selfWeight: int = Field(None)
    witnesses: List[Witness] = Field(None)


class LogParameters(BaseModel):
    prerotation: bool = Field(None)
    portable: bool = Field(None)
    updateKeys: List[str] = Field(None)
    nextKeyHashes: List[str] = Field(None)
    witness: WitnessParam = Field(None)
    deactivated: bool = Field(None)
    ttl: bool = Field(None)
    method: str = Field(None)
    scid: str = Field(None)


class InitialLogEntry(BaseModel):
    versionId: str = Field()
    versionTime: str = Field()
    parameters: LogParameters = Field()
    state: dict = Field()
    proof: Union[DataIntegrityProof, List[DataIntegrityProof]] = Field(None)


class LogEntry(BaseModel):
    versionId: str = Field()
    versionTime: str = Field()
    parameters: LogParameters = Field()
    state: DidDocument = Field()
    proof: Union[DataIntegrityProof, List[DataIntegrityProof]] = Field(None)
