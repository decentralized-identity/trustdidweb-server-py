from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models.web_schemas import RegisterDID
from config import settings
from app.plugins import AskarVerifier, AskarStorage
from app.dependencies import identifier_available, did_document_exists

router = APIRouter(tags=["Identifiers"])


@router.get("/")
async def request_did(
    namespace: str = None,
    identifier: str = None,
):
    if namespace and identifier:
        did = f"{settings.DID_WEB_BASE}:{namespace}:{identifier}"
        await identifier_available(did)
        return JSONResponse(
            status_code=200,
            content={
                "didDocument": {
                    "@context": ["https://www.w3.org/ns/did/v1"],
                    "id": did,
                },
                "proofOptions": AskarVerifier().create_proof_config(did),
            },
        )

    raise HTTPException(status_code=400, detail="Missing request information.")


@router.post("/{namespace}/{identifier}")
async def register_did(
    namespace: str,
    identifier: str,
    request_body: RegisterDID,
):
    did_document = request_body.model_dump()["didDocument"]
    did = f"{settings.DID_WEB_BASE}:{namespace}:{identifier}"

    await identifier_available(did)

    # Ensure correct endpoint is called
    if did_document["id"] != did:
        raise HTTPException(status_code=400, detail="Location mismatch.")

    # Assert proof set
    proof_set = did_document.pop("proof", None)
    if len(proof_set) != 2:
        raise HTTPException(status_code=400, detail="Expecting proof set.")

    # Find proof matching endorser
    endorser_proof = next(
        (
            proof
            for proof in proof_set
            if proof["verificationMethod"]
            == f"did:key:{settings.ENDORSER_MULTIKEY}#{settings.ENDORSER_MULTIKEY}"
        ),
        None,
    )

    # Find proof matching client
    client_proof = next(
        (
            proof
            for proof in proof_set
            if proof["verificationMethod"]
            != f"did:key:{settings.ENDORSER_MULTIKEY}#{settings.ENDORSER_MULTIKEY}"
        ),
        None,
    )

    if client_proof and endorser_proof:
        # Verify proofs
        AskarVerifier().verify_proof(did_document, client_proof)
        AskarVerifier().verify_proof(did_document, endorser_proof)
        authorized_key = client_proof["verificationMethod"].split("#")[-1]

        # TODO implement registration queue
        # await AskarStorage().store("didRegistration", did, did_document)

        # Store document and authorized key
        await AskarStorage().store("didDocument", did, did_document)
        await AskarStorage().store("authorizedKey", did, authorized_key)
        return JSONResponse(status_code=201, content={"didDocument": did_document})

    raise HTTPException(status_code=400, detail="Missing expected proof.")


@router.get("/{namespace}/{identifier}/did.json", include_in_schema=False)
async def get_did_document(namespace: str, identifier: str):
    did = f"{settings.DID_WEB_BASE}:{namespace}:{identifier}"
    did_doc = await AskarStorage().fetch("didDocument", did)
    if did_doc:
        return JSONResponse(status_code=200, content=did_doc)
    raise HTTPException(status_code=404, detail="Ressource not found.")
