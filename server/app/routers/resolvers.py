from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from config import settings
from app.plugins import AskarVerifier, AskarStorage, TrustDidWeb
from app.utilities import to_did_web, did_document_exists
import jsonlines
import json

router = APIRouter(tags=["Resolvers"])

@router.get("/.well-known/did.json")
async def get_endorser_did():
    did_document = await AskarStorage().fetch("didDocument", settings.DID_WEB_BASE)
    return JSONResponse(status_code=200, content=did_document)

@router.get("/{namespace}/{identifier}/did.json")
async def get_did(
    namespace: str, identifier: str
):
    did = to_did_web(namespace, identifier)
    await did_document_exists(did)
    did_document = await AskarStorage().fetch("didDocument", did)
    return JSONResponse(status_code=200, content=did_document)


@router.get("/{namespace}/{identifier}/did.jsonl")
async def get_did_logs(
    namespace: str, identifier: str, response: Response
):
    did = to_did_web(namespace, identifier)
    await did_document_exists(did)
    did_logs = await AskarStorage().fetch("didLogs", did)
    did_logs = jsonlines.Reader(did_logs).read()
    response.headers['Content-Type'] = 'application/octet-stream'
    return did_logs