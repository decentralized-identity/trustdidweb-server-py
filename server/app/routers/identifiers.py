from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from app.models.web_requests import RequestDID, RegisterDID, RequestDIDUpgrade, PublishLogEntry
from config import settings
from app.plugins import AskarVerifier, AskarStorage, TrustDidWeb
# from app.dependencies import (
#     did_document_exists,
#     valid_did_registration,
# )
from app.utilities import location_available, to_did_web, valid_did_registration, did_document_exists, bootstrap_did_doc
import jsonlines
import json

router = APIRouter(tags=["Identifiers"])


@router.post("/identifier/request", summary="Request new identifier.")
async def request_did(request_body: RequestDID):
    did = to_did_web(request_body.model_dump()['namespace'], request_body.model_dump()['identifier'])
    await location_available(did)
    return JSONResponse(
        status_code=200,
        content={
            "document": bootstrap_did_doc(did),
            "options": AskarVerifier().create_proof_config(),
        },
    )


@router.post("/identifier/register", summary="Register identifier.")
async def upgrade_did(request_body: RegisterDID):
    did_document = request_body.model_dump()['didDocument']
    await location_available(did_document['id'])
    await valid_did_registration(did_document)
    await AskarStorage().store("didDocument", did_document['id'], did_document)
    return JSONResponse(
        status_code=201,
        content={
            "didDocument": did_document,
        },
    )


@router.post("/identifier/upgrade", summary="Upgrade to Trust DID Web.")
async def request_did_upgrade(request_body: RequestDIDUpgrade):
    await did_document_exists(request_body.model_dump()['id'])
    did_document = await AskarStorage().fetch("didDocument", request_body.model_dump()['id'])
    log_entry = TrustDidWeb().provision_log_entry(did_document, request_body.model_dump()['updateKey'])
    return JSONResponse(
        status_code=200,
        content={
            "logEntry": log_entry,
            "proofOptions": AskarVerifier().create_proof_config(challenge=log_entry[0]),
        },
    )


@router.post("/identifier/log", summary="Publish log entry.")
async def publish_log(request_body: PublishLogEntry, response: Response):
    log_entry = request_body.model_dump()['logEntry']
    did_tdw = log_entry[3]['value']['id']
    did_web = 'did:web:'+':'.join(did_tdw.split(':')[3:])
    await did_document_exists(did_web)
    # await valid_log_entry(log_entry)
    did_document = await AskarStorage().fetch("didDocument", did_web)
    did_document['alsoKnownAs'] = log_entry[3]['value']['id']
    did_document = await AskarStorage().update("didDocument", did_web, did_document)
    logs = [json.dumps(log_entry)]
    did_document = await AskarStorage().store("didLogs", did_web, logs)
    return JSONResponse(status_code=201, content={'did': did_tdw})
