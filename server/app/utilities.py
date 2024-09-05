from app.models.did_documents import DidDocument
from config import settings
from pydid import DIDDocumentBuilder

def create_did_doc(did, multikey):
    return DidDocument(
        id=did,
        verificationMethod=[
            {
                "id": f"{did}#key-01",
                "type": "MultiKey",
                "controller": did,
                "publicKeyMultibase": multikey,
            }
        ],
        authentication=[f"{did}#key-01"],
        assertionMethod=[f"{did}#key-01"],
        service=[],
    ).dict(by_alias=True, exclude_none=True)

def create_did_doc_template(namespace, identifier):
    return DIDDocumentBuilder(
        f"{settings.DID_WEB_BASE}:{namespace}:{identifier}"
    ).build().serialize()
