from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/{id}/credentials/status/{cred_id}")
async def get_status_credential(id: str, cred_id: str):
    did_doc = {}
    return JSONResponse(status_code=200, content=did_doc)


@router.post("/{id}/credentials/status/{cred_id}")
async def create_status_credential(id: str, cred_id: str):
    pass


@router.put("/{id}/credentials/status/{cred_id}")
async def update_status_credential(id: str, cred_id: str):
    pass


@router.delete("/{id}/credentials/status/{cred_id}")
async def delete_status_credential(id: str, cred_id: str):
    pass
