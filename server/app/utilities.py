from app.models.did_document import DidDocument
from config import settings

def create_did_doc(did, multikey, kid='key-01'):
    return DidDocument(
        id=did,
        verificationMethod=[
            {
                "id": kid,
                "type": "MultiKey",
                "controller": did,
                "publicKeyMultibase": multikey,
            }
        ],
        authentication=[kid],
        assertionMethod=[kid],
        service=[],
    ).dict(by_alias=True, exclude_none=True)

def create_did_doc_template(namespace, identifier):
    return DidDocument(
        id=f"{settings.DID_WEB_BASE}:{namespace}:{identifier}",
    ).dict(by_alias=True, exclude_none=True)


def find_key(did_doc, kid):
    return next(
        (
            vm['publicKeyMultibase']
            for vm in did_doc["verificationMethod"]
            if vm["id"] == kid
        ),
        None,
    )


def find_proof(proofs, kid):
    return next(
        (
            proof
            for proof in proofs
            if proof["verificationMethod"] == kid
        ),
        None,
    )