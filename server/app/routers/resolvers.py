from fastapi import APIRouter, HTTPException, Response
from config import settings
from app.plugins import AskarStorage
import json

router = APIRouter(tags=["Resolvers"])


@router.get("/{namespace}/{identifier}/did.json", include_in_schema=False)
async def get_did_document(namespace: str, identifier: str):
    did = f"{settings.DID_WEB_BASE}:{namespace}:{identifier}"
    did_doc = await AskarStorage().fetch("didDocument", did)
    if did_doc:
        return Response(did_doc, media_type="application/ld+json")
    raise HTTPException(status_code=404, detail="Ressource not found.")


@router.get("/{namespace}/{identifier}/did.jsonl", include_in_schema=False)
async def get_did_logs(namespace: str, identifier: str):
    did = f"{settings.DID_WEB_BASE}:{namespace}:{identifier}"
    log_entries = await AskarStorage().fetch("logEntries", did)
    if log_entries:
        log_entries = "\n".join([json.dumps(log_entry) for log_entry in log_entries])
        return Response(log_entries, media_type="text/jsonl")
    raise HTTPException(status_code=404, detail="Ressource not found.")
