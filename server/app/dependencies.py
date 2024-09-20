from fastapi import HTTPException
from config import settings
from app.plugins import AskarStorage


async def identifier_available(namespace: str, identifier: str):
    if await AskarStorage().fetch("didDocument", f"{settings.DID_WEB_BASE}:{namespace}:{identifier}"):
        raise HTTPException(status_code=409, detail="Identifier unavailable.")


async def did_document_exists(namespace: str, identifier: str):
    if not await AskarStorage().fetch("didDocument", f"{settings.DID_WEB_BASE}:{namespace}:{identifier}"):
        raise HTTPException(status_code=404, detail="Ressource not found.")
