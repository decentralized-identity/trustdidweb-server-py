from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.models.web_requests import RegisterDID
from config import settings
from app.plugins import AskarVerifier, AskarStorage
from app.dependencies import (
    identifier_available,
    did_document_exists,
    valid_did_registration,
)
from app.utilities import create_did_doc_template

router = APIRouter()


@router.get("/{namespace}/{identifier}", summary="Request DID configuration.")
async def get_did(
    namespace: str, identifier: str, dependency=Depends(identifier_available)
):
    return JSONResponse(
        status_code=200,
        content={
            "document": create_did_doc_template(namespace, identifier),
            "options": AskarVerifier().create_proof_config(),
        },
    )


@router.post("/{namespace}/{identifier}", summary="Register DID.")
async def register_did(
    request_body: RegisterDID,
    namespace: str,
    identifier: str,
    did_document=Depends(valid_did_registration),
):
    await AskarStorage().store("didDocument", f"{namespace}:{identifier}", did_document)
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
async def get_did(
    namespace: str, identifier: str, dependency=Depends(did_document_exists)
):
    did_doc = await AskarStorage().fetch("didDocument", f"{namespace}:{identifier}")
    return JSONResponse(status_code=200, content=did_doc)
