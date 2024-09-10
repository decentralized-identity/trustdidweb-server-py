from app.models.did_document import DidDocument
from config import settings
from app.plugins import AskarVerifier, AskarStorage
from fastapi import HTTPException


def to_did_web(namespace: str, identifier: str):
    return f'{settings.DID_WEB_BASE}:{namespace}:{identifier}'


async def location_available(did: str):
    if await AskarStorage().fetch("didDocument", did):
        raise HTTPException(status_code=409, detail="Identifier unavailable.")


async def did_document_exists(did: str):
    if not await AskarStorage().fetch("didDocument", did):
        raise HTTPException(status_code=404, detail="Ressource not found.")


async def valid_did_registration(
    did_document
):
    did_document
    proofs = did_document.pop("proof")
    try:
        # assert (
        #     did_document["id"] == f"{settings.DID_WEB_BASE}:{namespace}:{identifier}"
        # ), "Id mismatch between DID Document and requested endpoint."
        assert (
            len(did_document["verificationMethod"]) >= 1
        ), "DID Documentmust contain at least 1 verificationMethod."
        assert (
            isinstance(proofs, list) and len(proofs) == 2
        ), "Insuficient proofs, must contain a client and an endorser proof."
    except AssertionError as msg:
        raise HTTPException(status_code=400, detail=str(msg))
    
    endorser_proof = find_proof(proofs, f"{settings.DID_WEB_BASE}#key-01")
    endorser_key = settings.ENDORSER_MULTIKEY
    AskarVerifier(endorser_key).verify_proof(did_document, endorser_proof)
    
    client_proof = find_proof(proofs, did_document["verificationMethod"][0]["id"])
    client_key = find_key(did_document, client_proof["verificationMethod"])
    AskarVerifier(client_key).verify_proof(did_document, client_proof)

    return did_document


async def identifier_available(identifier: str):
    if await AskarStorage().fetch("didDocument", identifier):
        raise HTTPException(status_code=409, detail="Identifier unavailable.")

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

def bootstrap_did_doc(did):
    return DidDocument(
        id=did,
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