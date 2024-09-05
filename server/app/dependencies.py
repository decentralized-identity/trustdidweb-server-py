from fastapi import HTTPException
from config import settings
from app.models.web_requests import RegisterDID
from app.plugins import AskarVerifier, AskarStorage
    

async def identifier_available(namespace: str, identifier: str):
    if await AskarStorage().fetch("didDocument", f'{namespace}:{identifier}'):
        raise HTTPException(status_code=409, detail="Identifier unavailable.")

async def did_document_exists(namespace: str, identifier: str):
    if not await AskarStorage().fetch("didDocument", f'{namespace}:{identifier}'):
        raise HTTPException(status_code=404, detail="Ressource not found.")

async def valid_did_registration(namespace: str, identifier: str, request_body: RegisterDID):
    document = request_body.model_dump(by_alias=True, exclude_none=True)['didDocument']
    proofs = document.pop('proof')
    try:
        assert document["id"] == f"{settings.DID_WEB_BASE}:{namespace}:{identifier}",\
            'Id mismatch between DID Document and requested endpoint.'
        assert len(document["verificationMethod"]) >= 1,\
            'DID Documentmust contain at least 1 verificationMethod.'
        assert isinstance(proofs, list) and len(proofs) == 2,\
            'Insuficient proofs, must contain a client and an endorser proof.'
    except AssertionError as msg:
        raise HTTPException(status_code=400, detail=str(msg))
    endorser_proof = next(
        (
            proof
            for proof in proofs
            if proof["verificationMethod"] == f"{settings.DID_WEB_BASE}#key-01"
        ),
        None,
    )
    endorser_key = settings.ENDORSER_MULTIKEY
    AskarVerifier(endorser_key).verify_proof(document, endorser_proof)
    client_proof = next(
        (
            proof
            for proof in proofs
            if proof["verificationMethod"]
            == document["verificationMethod"][0]["id"]
        ),
        None,
    )
    client_key = next(
        (
            vm["publicKeyMultibase"]
            for vm in document["verificationMethod"]
            if vm["id"] == client_proof["verificationMethod"]
        ),
        None,
    )
    AskarVerifier(client_key).verify_proof(document, client_proof)
    return document
