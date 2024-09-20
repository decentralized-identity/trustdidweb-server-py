from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.models.web_schemas import RegisterDID
from config import settings
from app.plugins import AskarVerifier, AskarStorage
from app.dependencies import (
    did_document_exists,
)
from app.plugins import AskarVerifier, AskarStorage

router = APIRouter()


@router.get("/", summary="Request DID configuration.")
async def request_did(
    namespace: str = None,
    identifier: str = None,
):
    if namespace and identifier:
        did = f"{settings.DID_WEB_BASE}:{namespace}:{identifier}"
        if await AskarStorage().fetch("didDocument", did):
            raise HTTPException(
                status_code=409, detail="Requested identifier unavailable."
            )

        return JSONResponse(
            status_code=200,
            content={
                "id": did,
                "proofOptions": AskarVerifier().create_proof_config(did),
            },
        )

    raise HTTPException(status_code=418)


@router.post("/", summary="Register DID.")
async def register_did(
    request_body: RegisterDID,
):
    did_document = request_body.model_dump()['didDocument']
    
    # Extract and verify the proofs
    proof_set = did_document.pop("proof", None)
    for proof in proof_set:
        AskarVerifier().verify_proof(did_document, proof)
        if proof['verificationMethod'].startswith('did:key:'):
            authorized_key = proof['verificationMethod'].split('#')[-1]
            
    # Ensure DID is available
    did = did_document["id"]
    if await AskarStorage().fetch("didDocument", did):
        raise HTTPException(
            status_code=409, detail="Requested identifier unavailable."
        )
        
    # Store document and authorized key
    await AskarStorage().store("didDocument", did, did_document)
    await AskarStorage().store("authorizedKey", did, authorized_key)
    return JSONResponse(status_code=201, content={"didDocument": did_document})


@router.put("/{namespace}/{identifier}", summary="Update DID document.")
async def update_did(
    namespace: str, identifier: str, dependency=Depends(did_document_exists)
):
    raise HTTPException(status_code=501, detail="Not implemented.")


@router.delete("/{namespace}/{identifier}", summary="Archive DID.")
async def delete_did(
    namespace: str, identifier: str, dependency=Depends(did_document_exists)
):
    raise HTTPException(status_code=501, detail="Not implemented.")


@router.get("/{namespace}/{identifier}/did.json", summary="Get DID document.")
async def get_did_document(
    namespace: str, identifier: str, dependency=Depends(did_document_exists)
):
    did = f"{settings.DID_WEB_BASE}:{namespace}:{identifier}"
    did_doc = await AskarStorage().fetch("didDocument", did)
    if did_doc:
        return JSONResponse(status_code=200, content=did_doc)
    raise HTTPException(status_code=404, detail="Ressource not found.")
