from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models.web_requests import RegisterDID
from config import settings
from datetime import datetime, timezone
from app.db import AskarStorage
from app.auth import verify_assertion_proof, verify_auth_proof
import uuid

router = APIRouter()


@router.get("/{identifier}", summary="Request DID configuration.")
async def get_did(identifier: str):
    if await AskarStorage().fetch("didDocument", identifier):
        raise HTTPException(status_code=409, detail="Identifier unavailable.")
    timestamp = str(datetime.now(timezone.utc).isoformat("T", "seconds"))
    return JSONResponse(
        status_code=200,
        content={
            "didDocument": {
                "@context": ["https://www.w3.org/ns/did/v1"],
                "id": f"{settings.DID_WEB_BASE}:{identifier}",
                "verificationMethod": [],
                "authentication": [],
                "assertionMethod": [],
                "service": [],
            },
            "proofConfig": {
                "type": "DataIntegrityProof",
                "cryptosuite": "eddsa-jcs-2022",
                "created": timestamp,
                "domain": settings.DID_WEB_BASE.split(":")[-1],
                "challenge": str(uuid.uuid5(settings.CHALLENGE_SALT, timestamp)),
            },
        },
    )


@router.post("/{identifier}", summary="Register DID.")
async def register_did(request_body: RegisterDID, identifier: str):
    if await AskarStorage().fetch("didDocument", identifier):
        raise HTTPException(status_code=409, detail="Identifier unavailable.")
    did_doc = vars(request_body)['didDocument']
    try:
        assert did_doc['id'] == f"{settings.DID_WEB_BASE}:{identifier}"
        assert len(did_doc['verificationMethod']) >= 1
    except:
        raise HTTPException(status_code=400, detail="Invalid DID Document.")
    
    proofs = did_doc.pop("proof", None)
    auth_proof = next(
        (proof for proof in proofs if proof["verificationMethod"] == f'{settings.DID_WEB_BASE}#multikey'),
        None,
    )
    verify_auth_proof(did_doc, auth_proof)
    assertion_proof = next(
        (proof for proof in proofs if proof["verificationMethod"] == did_doc['verificationMethod'][0]['id']),
        None,
    )
    verify_assertion_proof(did_doc, assertion_proof)
    await AskarStorage().store("didDocument", identifier, did_doc)
    return JSONResponse(status_code=201, content=did_doc)


@router.get("/{identifier}/did.json", summary="Get DID document.")
async def get_did(identifier: str):
    did_doc = await AskarStorage().fetch("didDocument", identifier)
    if not did_doc:
        raise HTTPException(status_code=404, detail="Ressource not found.")
    return JSONResponse(status_code=200, content=did_doc)


@router.put("/{identifier}/did.json", summary="Update DID document.")
async def update_did(id: str):
    pass


@router.delete("/{identifier}/did.json", summary="Archive DID.")
async def delete_did(id: str):
    pass
