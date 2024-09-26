from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.models.web_schemas import RegisterDID
from config import settings
from app.plugins import AskarVerifier, AskarStorage
from app.plugins import AskarVerifier, AskarStorage

router = APIRouter(prefix="/registrations")


@router.get("/", summary="Request registration queue.")
async def fetch_did_registration(
    did: str = None
):
    if did:
        if await AskarStorage().fetch("didRegistration", did):
            raise HTTPException(
                status_code=409, detail="Requested identifier unavailable."
            )
    else:
        if await AskarStorage().fetch("didRegistration", did):
            raise HTTPException(
                status_code=409, detail="Requested identifier unavailable."
            )

    return JSONResponse(
        status_code=200,
        content={},
    )


@router.delete("/#{did}", summary="Request registration queue.")
async def delete_did_registration(
    did: str = None
):
    pass