from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from app.routers import identifiers, status_lists
from config import settings

app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)


api_router = APIRouter()


@api_router.get("/.well-known/did.json", tags=["Server"])
async def witness_did_doc():
    did_doc = {
        "@context": [
            "https://www.w3.org/ns/did/v1",
            "https://w3id.org/security/multikey/v1"
        ],
        "id": "did:web:identifier.me",
        "verificationMethod": [
            {
                "id": "did:web:identifier.me#multikey",
                "type": "MultiKey",
                "controller": "did:web:identifier.me",
                "publicKeyMultibase": settings.WITNESS_MULTIKEY
            }
        ],
        "authentication": [
            "did:web:identifier.me#jwk"
        ],
        "assertionMethod": [
            "did:web:identifier.me#jwk"
        ],
        "service": []
    }
    return JSONResponse(status_code=200, content=did_doc)

api_router.include_router(identifiers.router, tags=["Identifiers"])
# api_router.include_router(status_lists.router, tags=["BitstringStatusList"])


@api_router.get("/server/status", tags=["Server"])
async def server_status():
    return JSONResponse(status_code=200, content={"status": "ok"})


app.include_router(api_router)
