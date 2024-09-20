from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from app.routers import identifiers
from config import settings
from app.plugins import AskarStorage

app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)


api_router = APIRouter()


@api_router.get("/server/status", tags=["Server"], include_in_schema=False)
async def server_status():
    return JSONResponse(status_code=200, content={"status": "ok"})


@api_router.get("/.well-known/did.json", tags=["Server"], include_in_schema=False)
async def get_main_did_document():
    did_document = await AskarStorage().fetch("didDocument", settings.DID_WEB_BASE)
    return JSONResponse(status_code=200, content=did_document)


api_router.include_router(identifiers.router, tags=["Identifiers"])


app.include_router(api_router)
